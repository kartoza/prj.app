# coding=utf-8
import StringIO
import os
import zipfile
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from ..models import Certificate, Course, Attendee, CertifyingOrganisation
from ..forms import CertificateForm
from base.models.project import Project


class CertificateMixin(object):
    """Mixin class to provide standard settings for Certificate."""

    model = Certificate
    form_class = CertificateForm


class CertificateCreateView(
        LoginRequiredMixin, CertificateMixin, CreateView):
    """Create view for Certificate."""

    context_object_name = 'certificate'
    template_name = 'certificate/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Course detail page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('course-detail', kwargs={
            'project_slug': self.project_slug,
            'organisation_slug': self.organisation_slug,
            'slug': self.course_slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CertificateCreateView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.course_slug)
        context['attendee'] = Attendee.objects.get(pk=self.pk)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CertificateCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.course_slug = self.kwargs.get('course_slug', None)
        self.pk = self.kwargs.get('pk', None)
        self.course = Course.objects.get(slug=self.course_slug)
        self.attendee = Attendee.objects.get(pk=self.pk)
        kwargs.update({
            'user': self.request.user,
            'course': self.course,
            'attendee': self.attendee,
        })
        return kwargs

    def form_valid(self, form):
        """Save new created certificate

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect

        We check that there is no referential integrity error when saving."""

        try:
            super(CertificateCreateView, self).form_valid(form)

            # Update organisation credits every time a certificate is issued.
            organisation = \
                CertifyingOrganisation.objects.get(
                    slug=self.organisation_slug)
            remaining_credits = \
                organisation.organisation_credits - \
                organisation.project.certificate_credit
            organisation.organisation_credits = remaining_credits
            organisation.save()

            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                'ERROR: Certificate already exists!')


class CertificateDetailView(DetailView):
    """Detail view for Certificate."""

    model = Certificate
    context_object_name = 'certificate'
    template_name = 'certificate/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.certificateID = self.kwargs.get('id', None)
        self.project_slug = self.kwargs.get('project_slug', None)
        context = super(
            CertificateDetailView, self).get_context_data(**kwargs)
        issued_id = \
            Certificate.objects.all().values_list('certificateID', flat=True)
        if self.certificateID in issued_id:
            context['certificate'] = \
                Certificate.objects.get(certificateID=self.certificateID)
        context['project_slug'] = self.project_slug
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all certificate in the
            corresponding organisation.
        :rtype: QuerySet
        """

        qs = Certificate.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a certificate
            depends on the input certificate ID.
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            certificateID = self.kwargs.get('id', None)
            if certificateID:
                try:
                    obj = queryset.get(certificateID=certificateID)
                    return obj
                except Certificate.DoesNotExist:
                    return None
            else:
                raise Http404('Sorry! Certificate by this ID is not exist.')


def certificate_pdf_view(request, **kwargs):

    project_slug = kwargs.pop('project_slug')
    course_slug = kwargs.pop('course_slug')
    pk = kwargs.pop('pk')
    project = Project.objects.get(slug=project_slug)
    course = Course.objects.get(slug=course_slug)
    attendee = Attendee.objects.get(pk=pk)
    certificate = Certificate.objects.get(course=course, attendee=attendee)
    current_site = request.META['HTTP_HOST']

    # Create the HttpResponse object with the appropriate PDF headers.
    filename = '{}.{}'.format(certificate.certificateID, 'pdf')
    project_folder = (project.name.lower()).replace(' ', '_')
    pathname = \
        os.path.join(
            '/home/web/media', 'pdf/{}/{}'.format(project_folder, filename))
    found = os.path.exists(pathname)
    if found:
        with open(pathname, 'r') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = \
                'filename={}.pdf'.format(certificate.certificateID)
            return response
    else:
        makepath = '/home/web/media/pdf/{}/'.format(project_folder)
        if not os.path.exists(makepath):
            os.makedirs(makepath)

        # Create the PDF object, using the response object as its "file."
        page = canvas.Canvas(pathname, pagesize=landscape(A4))
        width, height = A4
        center = height * 0.5

        if project.image_file:
            project_logo = ImageReader(project.image_file)
        else:
            project_logo = None

        if course.certifying_organisation.logo:
            organisation_logo = ImageReader(
                course.certifying_organisation.logo)
        else:
            organisation_logo = None

        if project.signature:
            project_owner_signature = ImageReader(project.signature)
        else:
            project_owner_signature = None

        if course.course_convener.signature:
            convener_signature = ImageReader(course.course_convener.signature)
        else:
            convener_signature = None

        if course.template_certificate:
            background = ImageReader(course.template_certificate)
        else:
            background = None

        # Certificate margin.
        margin_right = height - 50
        margin_left = 50
        margin_bottom = 50
        max_left = margin_right - 100

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        if background is not None:
            page.drawImage(
                background, 0, 0, height=width, width=height,
                preserveAspectRatio=True, mask='auto')
        page.setFillColorRGB(0.1, 0.1, 0.1)
        page.setFont('Times-Roman', 18)
        # page.drawString(margin_left, 480, project.name)
        # page.drawRightString(
        #     (margin_right), 480, course.certifying_organisation.name)

        if project_logo is not None:
            page.drawImage(
                project_logo, 50, 450, width=100, height=100,
                preserveAspectRatio=True, mask='auto')

        if organisation_logo is not None:
            page.drawImage(
                organisation_logo, max_left, 450, height=100, width=100,
                preserveAspectRatio=True, anchor='c', mask='auto')

        page.setFont('Times-Bold', 26)
        page.drawCentredString(center, 480, 'Certificate of Completion')
        page.drawCentredString(
            center, 400, '%s %s' % (attendee.firstname, attendee.surname))
        page.setFont('Times-Roman', 16)
        page.drawCentredString(
            center, 360, 'Has attended and completed the course:')
        page.setFont('Times-Bold', 20)
        page.drawCentredString(center, 300, course.course_type.name)
        page.setFont('Times-Roman', 16)
        page.drawCentredString(
            center, 270,
            'From {} {} {} to {} {} {}'
            .format(
                course.start_date.day,
                course.start_date.strftime('%B'),
                course.start_date.year,
                course.end_date.day,
                course.end_date.strftime('%B'),
                course.end_date.year))
        page.setFillColorRGB(0.1, 0.1, 0.1)
        page.drawCentredString(
            center, 220, 'Convened by {} {} at {}' .format(
                course.course_convener.user.first_name,
                course.course_convener.user.last_name,
                course.training_center))

        if project_owner_signature is not None:
            page.drawImage(
                project_owner_signature,
                (margin_left + 100),
                (margin_bottom + 70),
                width=100,
                height=70,
                preserveAspectRatio=True,
                anchor='s',
                mask='auto')

        if convener_signature is not None:
            page.drawImage(
                convener_signature, (margin_right - 200), (margin_bottom + 70),
                width=100, height=70, preserveAspectRatio=True, anchor='s',
                mask='auto')

        page.setFont('Times-Italic', 12)
        page.drawCentredString(
            (margin_left + 150), (margin_bottom + 60),
            '{} {}' .format(project.owner.first_name, project.owner.last_name))
        page.drawCentredString(
            (margin_right - 150), (margin_bottom + 60),
            '{} {}' .format(
                course.course_convener.user.first_name,
                course.course_convener.user.last_name))
        page.line(
            (margin_left + 70), (margin_bottom + 55),
            (margin_left + 230), (margin_bottom + 55))
        page.line(
            (margin_right - 70), (margin_bottom + 55),
            (margin_right - 230), (margin_bottom + 55))
        page.setFont('Times-Roman', 13)
        page.drawCentredString(
            (margin_left + 150),
            (margin_bottom + 40),
            'Project Representative')
        page.drawCentredString(
            (margin_right - 150), (margin_bottom + 40), 'Course Convener')

        # Footnotes.
        page.setFont('Times-Roman', 14)
        page.drawString(
            margin_left,
            margin_bottom - 10,
            'ID: {}'.format(certificate.certificateID))
        page.setFont('Times-Roman', 8)
        page.drawString(
            margin_left, (margin_bottom - 20),
            'You can verify this certificate by visiting '
            'http://{}/en/{}/certificate/{}/.'
            .format(current_site, project.slug, certificate.certificateID))

        # Close the PDF object cleanly.
        page.showPage()
        page.save()
        with open(pathname, 'r') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = \
                'filename={}.pdf'.format(certificate.certificateID)
            return response


def download_certificates_zip(request, **kwargs):
    """Download all certificates in a course as one zip file."""

    project_slug = kwargs.pop('project_slug')
    course_slug = kwargs.pop('course_slug')
    course = Course.objects.get(slug=course_slug)
    organisation_slug = kwargs.pop('organisation_slug')

    certificates = Certificate.objects.filter(course=course)

    filenames = []
    for certificate in certificates:
        pdf_file = certificate_pdf_view(
            request, pk=certificate.attendee.pk, project_slug=project_slug,
            course_slug=course_slug, organisation_slug=organisation_slug)

        with open('/tmp/%s.pdf' % certificate.certificateID, 'wb') as pdf:
            pdf.write(pdf_file.content)

        filenames.append('/tmp/%s.pdf' % certificate.certificateID)

    zip_subdir = '%s' % course.name

    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        zf.write(fpath, zip_path)

    zf.close()

    response = HttpResponse(
        s.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = \
        'attachment; filename=certificates.zip'

    return response


def update_paid_status(request, **kwargs):
    """View to update the is_paid status of certificate in a course."""

    project_slug = kwargs.pop('project_slug')
    organisation_slug = kwargs.pop('organisation_slug')
    course_slug = kwargs.pop('course_slug')
    attendee_pk = kwargs.pop('pk')
    course = Course.objects.get(slug=course_slug)
    attendee = Attendee.objects.get(pk=attendee_pk)
    project = Project.objects.get(slug=project_slug)
    url = reverse('course-detail', kwargs={
            'project_slug': project_slug,
            'organisation_slug': organisation_slug,
            'slug': course_slug
    })

    if request.method == 'POST':
        queryset = \
            Certificate.objects.filter(course=course, attendee=attendee)
        queryset.update(is_paid=True)
        organisation = \
            CertifyingOrganisation.objects.get(slug=organisation_slug)
        remaining_credits = \
            organisation.organisation_credits - project.certificate_credit
        organisation.organisation_credits = remaining_credits
        organisation.save()
        return HttpResponseRedirect(url)

    return render(
        request, 'certificate/update_is_paid.html',
        context={
            'course': course,
            'project_slug': project_slug,
            'organisation_slug': organisation_slug,
            'course_slug': course_slug,
            'attendee': attendee,
            'project': project})


def top_up_unavailable(request, **kwargs):
    project_slug = kwargs.get('project_slug', None)
    project = Project.objects.get(slug=project_slug)
    organisation = CertifyingOrganisation.objects.filter(approved=False)
    has_pending = False
    if organisation:
        has_pending = True

    return render(
        request, 'certificate/top_up_unavailable.html',
        context={
            'the_project': project,
            'has_pending_organisations': has_pending})


def email_all_attendees(request, **kwargs):
    project_slug = kwargs.get('project_slug', None)
    course_slug = kwargs.get('course_slug', None)
    organisation_slug = kwargs.get('organisation_slug', None)
    project = Project.objects.get(slug=project_slug)
    course = Course.objects.get(slug=course_slug)
    attendee_list = \
        Certificate.objects.filter(
            is_paid=True, course=course).values_list('attendee', flat=True)
    attendee_list_object = []
    for attendee_pk in attendee_list:
        attendee = Attendee.objects.get(pk=attendee_pk)
        attendee_list_object.append(attendee)

    organisation = CertifyingOrganisation.objects.filter(approved=False)
    has_pending = False
    if organisation:
        has_pending = True

    url = reverse('course-detail', kwargs={
        'project_slug': project_slug,
        'organisation_slug': organisation_slug,
        'slug': course_slug
    })

    if request.method == 'POST':

        site = request.get_host()
        for attendee in attendee_list_object:
            # Send email to each attendee with the link to his certificate.
            data = {
                'firstname': attendee.firstname,
                'lastname': attendee.surname,
                'coursetype': course.course_type,
                'start_date': course.start_date.strftime('%d %B %Y'),
                'end_date': course.end_date.strftime('%d %B %Y'),
                'training_center': course.training_center,
                'organisation': course.certifying_organisation.name,
                'domain': site,
                'project_slug': course.certifying_organisation.project.slug,
                'organisation_slug': course.certifying_organisation.slug,
                'course_slug': course.slug,
                'pk': attendee.pk,
                'convener_firstname': course.course_convener.user.first_name,
                'convener_lastname': course.course_convener.user.last_name}

            send_mail(
                'Certificate from {} Course'.format(course.course_type),
                'Dear {firstname} {lastname},\n\n'
                'Congratulations!\n'
                'Your certificate from the following course '
                'has been issued.\n\n'
                'Course type: {coursetype}\n'
                'Course date: {start_date} to {end_date}\n'
                'Training center: {training_center}\n'
                'Certifying organisation: {organisation}\n\n'
                'You may print the certificate '
                'by visiting:\n'
                'http://{domain}/en/{project_slug}/certifyingorganisation/'
                '{organisation_slug}/course/'
                '{course_slug}/print/{pk}/\n\n'
                'Sincerely,\n{convener_firstname} {convener_lastname}'
                .format(**data),
                course.course_convener.user.email,
                [attendee.email],
                fail_silently=False,
            )

        messages.success(request, 'Email sent', 'email_sent')
        return HttpResponseRedirect(url)

    return render(
        request, 'certificate/send_email_confirm.html',
        context={
            'the_project': project,
            'has_pending_organisations': has_pending,
            'attendees': attendee_list_object})
