# coding=utf-8
import cStringIO
from datetime import datetime
import os
from PIL import Image
import re
from unidecode import unidecode
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.text import slugify
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfgen import canvas
from core.settings.contrib import STOP_WORDS


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
    max_left = margin_right - 100

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
                project.project_representative.first_name.encode('utf-8'),
                project.project_representative.last_name.encode('utf-8')))
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
        'http://{}/en/{}/certificate/{}/.'
        .format(current_site, project.slug, certificate.certificateID))

    # Close the PDF object cleanly.
    page.showPage()
    page.save()


class DummyCertificate(object):
    """Dummy Certificate object for preview certificate."""

    def __init__(self, certifying_organisation):
        self.certificateID = \
            '{}-1'.format(certifying_organisation.project.name)
        self.certifying_organisation = certifying_organisation


class DummyCertifyingOrganisation(object):
    """Dummy Certifying Organisation object for preview certificate."""

    def __init__(self, project):
        self.project = project
        self.name = 'Test Organisation'


class DummyProject(object):
    """Dummy Project object for preview certificate."""

    def __init__(
            self,
            name,
            image_file,
            template,
            project_representative_signature,
            project_representative):

        self.name = name
        self.image_file = image_file
        self.template_certifying_organisation_certificate = template
        self.project_representative_signature = \
            project_representative_signature
        self.project_representative=project_representative
        words = self.name.split()
        filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
        # unidecode() represents special characters (unicode data) in ASCII
        new_list = unidecode(' '.join(filtered_words))
        self.slug = slugify(new_list)[:50]


def preview_certificate(request, **kwargs):
    """Generate pdf for certifying organisation in preview
    upon creating new project.

    """

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="preview.pdf"'
    project_name = request.POST.get('project_name', None)
    raw_logo = request.POST.get('project_logo', None)
    logo = None
    if raw_logo:
        if 'base64' in raw_logo:
            image_data = \
                re.sub('^data:image/.+;base64,', '', raw_logo).decode('base64')
            logo = Image.open(cStringIO.StringIO(image_data))

    raw_signature = request.POST.get('project_representative_signature', None)
    project_representative_signature = None
    if raw_signature:
        if 'base64' in raw_signature:
            image_signature = \
                re.sub(
                    '^data:image/.+;base64,', '', raw_signature
                ).decode('base64')
            project_representative_signature = \
                Image.open(cStringIO.StringIO(image_signature))

    if project_name:
        raw_image = request.POST.get('template_certificate', None)
        template_certificate = None
        if raw_image:
            if 'base64' in raw_image:
                image_data = \
                    re.sub(
                        '^data:image/.+;base64,', '', raw_image
                    ).decode('base64')
                template_certificate = \
                    Image.open(cStringIO.StringIO(image_data))

        project_representative_id = \
            request.POST.get('project_representative', None)
        project_representative = User.objects.get(id=project_representative_id)

        project = DummyProject(
            name=project_name,
            image_file=logo,
            template=template_certificate,
            project_representative_signature=project_representative_signature,
            project_representative=project_representative
        )

        certifying_organisation = DummyCertifyingOrganisation(
            project=project
        )

        certificate = DummyCertificate(
            certifying_organisation=certifying_organisation
        )

        current_site = request.META['HTTP_HOST']

        generate_certificate_pdf(
            response,
            project,
            certifying_organisation,
            certificate,
            current_site
        )

    else:
        # When preview page is refreshed, the data is gone so user needs to
        # go back to create page.

        page = canvas.Canvas(response, pagesize=landscape(A4))
        width, height = A4
        center = height * 0.5
        page.setFillColorRGB(0.1, 0.1, 0.1)
        page.setFont('Times-Roman', 16)
        page.drawCentredString(
            center, 360,
            'To preview your certificate template, '
            'please go to create new project page')
        page.drawCentredString(
            center, 335, 'and click on Preview Certificate button.')
        page.showPage()
        page.save()

    return response
