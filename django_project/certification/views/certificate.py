# coding=utf-8
from django.http import Http404, HttpResponse
from django.views.generic import CreateView, DetailView, ListView
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from pure_pagination.mixins import PaginationMixin
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

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="certificate.pdf"'

    # Create the PDF object, using the response object as its "file."
    page = canvas.Canvas(response, pagesize=landscape(A4))
    width, height = A4
    center = height * 0.5

    if project.image_file:
        project_logo = ImageReader(project.image_file)
    else:
        project_logo = None

    if course.certifying_organisation.logo:
        organisation_logo = ImageReader(course.certifying_organisation.logo)
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
    max_left = margin_right - 50

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
            project_logo, 50, 500, width=50, height=50,
            preserveAspectRatio=True, mask='auto')

    if organisation_logo is not None:
        page.drawImage(
            organisation_logo, max_left, 500, height=50, width=50,
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
        'From %s %s %s to %s %s %s'
        % (course.start_date.day, course.start_date.strftime('%B'),
           course.start_date.year, course.end_date.day,
           course.end_date.strftime('%B'), course.end_date.year))
    page.setFillColorRGB(0.1, 0.1, 0.1)
    page.drawCentredString(
        center, 220, 'Convened by %s %s at %s' % (
            course.course_convener.user.first_name,
            course.course_convener.user.last_name, course.training_center))

    if project_owner_signature is not None:
        page.drawImage(
            project_owner_signature,
            (margin_left + 100), (margin_bottom + 70), width=100, height=70,
            preserveAspectRatio=True, anchor='s', mask='auto')

    if convener_signature is not None:
        page.drawImage(
            convener_signature, (margin_right - 200), (margin_bottom + 70),
            width=100, height=70, preserveAspectRatio=True, anchor='s',
            mask='auto')

    page.setFont('Times-Italic', 12)
    page.drawCentredString(
        (margin_left + 150), (margin_bottom + 60),
        '%s %s' % (project.owner.first_name, project.owner.last_name))
    page.drawCentredString(
        (margin_right - 150), (margin_bottom + 60),
        '%s %s' % (
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
        (margin_left + 150), (margin_bottom + 40), 'Project Owner')
    page.drawCentredString(
        (margin_right - 150), (margin_bottom + 40), 'Convener')

    # Footnotes.
    page.setFont('Times-Roman', 14)
    page.drawString(
        margin_left, margin_bottom - 10, 'ID: %s' % certificate.certificateID)
    page.setFont('Times-Roman', 8)
    page.drawString(
        margin_left, (margin_bottom - 20),
        'You can verify this certificate by visiting /%s/certificate/%s/.'
        % (project.slug, certificate.certificateID))

    # Close the PDF object cleanly.
    page.showPage()
    page.save()
    return response


class UnpaidCertificateListView(
        ListView):
    """List view for unpaid certificates."""

    model = Certificate
    context_object_name = 'unpaidcertificates'
    template_name = 'certificate/unpaid_certificate.html'

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all certificate in the
            corresponding organisation.
        :rtype: QuerySet
        """

        qs = Certificate.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            UnpaidCertificateListView, self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
            context['project'] = context['the_project']
        context['organisations'] = \
            CertifyingOrganisation.objects.filter(
                project=context['project'], approved=True)
        num_unpaidcertificates = {}
        for organisation in context['organisations']:
            num_unpaidcertificates[organisation.name] = \
                Certificate.objects.filter(
                    course__certifying_organisation=organisation).count()
        context['num_unpaidcertificates'] = num_unpaidcertificates

        return context
