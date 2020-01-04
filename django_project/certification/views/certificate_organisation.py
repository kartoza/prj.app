# coding=utf-8
import os
from datetime import datetime
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse
from django.http import Http404, FileResponse
from django.views.generic import CreateView, DetailView
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from base.models.project import Project
from certification.models.certifying_organisation import CertifyingOrganisation
from certification.models.organisation_certificate import \
    CertifyingOrganisationCertificate
from certification.forms import OrganisationCertificateForm


def generate_certificate_pdf(
        pathname, project, certifying_organisation, certificate, current_site):
    """Create the PDF object, using the response object as its file."""

    # Register new font
    try:
        font_folder = os.path.join(
            settings.STATIC_ROOT, 'fonts/NotoSans-hinted')
        ttf_file = os.path.join(font_folder, 'NotoSans-Bold.ttf')
        pdfmetrics.registerFont(TTFont('Noto-bold', ttf_file))
    except TTFError:
        pass

    page = canvas.Canvas(pathname, pagesize=landscape(A4))
    width, height = A4
    center = height * 0.5

    if project.image_file:
        project_logo = ImageReader(project.image_file)
    else:
        project_logo = None

    if project.project_representative_signature:
        project_representative_signature = \
            ImageReader(project.project_representative_signature)
    else:
        project_representative_signature = None

    if project.template_certifying_organisation_certificate:
        background = \
            ImageReader(project.template_certifying_organisation_certificate)
    else:
        background = None

    # Certificate margin.
    margin_right = height - 50
    margin_left = 50
    margin_bottom = 50

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    if background is not None:
        page.drawImage(
            background, 0, 0, height=width, width=height,
            preserveAspectRatio=True, mask='auto')
    page.setFillColorRGB(0.1, 0.1, 0.1)
    page.setFont('Times-Roman', 18)

    if project_logo is not None:
        page.drawImage(
            project_logo, 50, 450, width=100, height=100,
            preserveAspectRatio=True, mask='auto')

    page.setFont('Times-Roman', 12)
    date_now = datetime.now()
    str_date = date_now.strftime("%m/%d/%Y")
    page.drawRightString(
        margin_right, width - 50, 'Date issued: {}'.format(str_date))

    try:
        page.setFont('Noto-bold', 26)
    except KeyError:
        page.setFont('Times-Bold', 26)

    page.drawCentredString(
        center, 350, '{}'.format(certifying_organisation.name))
    page.setFont('Times-Roman', 16)
    page.drawCentredString(
        center, 320,
        'Is authorized to provide {} training and certification.'.format(
            project.name))

    page.setFillColorRGB(0.1, 0.1, 0.1)
    if project_representative_signature is not None:
        page.drawImage(
            project_representative_signature,
            (margin_right - 200), (margin_bottom + 70),
            width=100,
            height=70,
            preserveAspectRatio=True,
            anchor='s',
            mask='auto')

    page.setFont('Times-Italic', 12)
    if project.project_representative:
        page.drawCentredString(
            (margin_right - 150), (margin_bottom + 60),
            '{} {}'.format(
                project.project_representative.first_name,
                project.project_representative.last_name))
    page.line(
        (margin_right - 70), (margin_bottom + 55),
        (margin_right - 230), (margin_bottom + 55))
    page.setFont('Times-Roman', 13)
    page.drawCentredString(
        (margin_right - 150),
        (margin_bottom + 40),
        'Project Representative')

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
        'http://{}/en/{}/organisationcertificate/{}/.'
        .format(current_site, project.slug, certificate.certificateID))

    # Close the PDF object cleanly.
    page.showPage()
    page.save()


class OrganisationCertificateCreateView(LoginRequiredMixin, CreateView):
    """Create view for Certificate for Certifying Organisation."""

    model = CertifyingOrganisationCertificate
    form_class = OrganisationCertificateForm
    context_object_name = 'certificate'
    template_name = 'certificate_organisation/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Course detail page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('certifyingorganisation-list', kwargs={
            'project_slug': self.project_slug,
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            OrganisationCertificateCreateView, self).get_context_data(**kwargs)
        context['certifying_organisation'] = self.certifying_organisation
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            OrganisationCertificateCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation
        })
        return kwargs


def organisation_certificate_pdf_view(request, **kwargs):
    project_slug = kwargs.pop('project_slug')
    organisation_slug = kwargs.pop('organisation_slug')
    project = Project.objects.get(slug=project_slug)
    certifying_organisation = \
        CertifyingOrganisation.objects.get(slug=organisation_slug)
    certificate = \
        CertifyingOrganisationCertificate.objects.get(
            certifying_organisation=certifying_organisation
        )
    current_site = request.META['HTTP_HOST']

    # Create the HttpResponse object with the appropriate PDF headers.
    filename = '{}.{}'.format(certificate.certificateID, 'pdf')
    project_folder = (project.name.lower()).replace(' ', '_')
    pathname = \
        os.path.join(
            '/home/web/media',
            'certificate_organisations/{}/{}'.format(
                project_folder, filename))
    makepath = \
        '/home/web/media/certificate_organisations/{}/'.format(
            project_folder)
    if not os.path.exists(makepath):
        os.makedirs(makepath)

    generate_certificate_pdf(
        pathname=pathname,
        certificate=certificate,
        project=project,
        certifying_organisation=certifying_organisation,
        current_site=current_site
    )
    try:
        return FileResponse(open(pathname, 'rb'),
                            content_type='application/pdf')
    except FileNotFoundError:  # noqa: F821
        raise Http404('Not found')


class OrganisationCertificateDetailView(DetailView):
    """Detail view for Certificate."""

    model = CertifyingOrganisationCertificate
    context_object_name = 'certificate'
    template_name = 'certificate_organisation/detail.html'

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
            OrganisationCertificateDetailView, self).get_context_data(**kwargs)
        context['project_slug'] = self.project_slug
        try:
            context['history'] = \
                context['certificate'].history.all().order_by('history_date')
        except KeyError:
            pass

        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all certificate in the
            corresponding project.
        :rtype: QuerySet
        """

        qs = CertifyingOrganisationCertificate.objects.all()
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
                except CertifyingOrganisationCertificate.DoesNotExist:
                    return None
            else:
                raise Http404('Sorry! Certificate by this ID does not exist.')
