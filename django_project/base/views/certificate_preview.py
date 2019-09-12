# coding=utf-8
import cStringIO
from PIL import Image
import re
from unidecode import unidecode
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.text import slugify
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from core.settings.contrib import STOP_WORDS
from certification.views.certificate_organisation import \
    generate_certificate_pdf


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
        self.project_representative = project_representative
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
