import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from changes.forms import SponsorForm

from base.tests.model_factories import ProjectF
from core.model_factories import UserF


class TestSponsorForm(TestCase):
    """Test uploading SVG file"""

    def setUp(self):
        self.user = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        self.project = ProjectF.create()
        self.svg = os.path.join(
            os.path.dirname(__file__), 'testfiles', 'qgis.svg')
        self.svg_content = open(self.svg, 'rb')
        self.webp = os.path.join(
            os.path.dirname(__file__), 'testfiles', 'qgis.webp')
        self.webp_content = open(self.webp, 'rb')

    def tearDown(self):
        self.svg_content.close()
        self.webp_content.close()

    def test_upload_svg_file(self):
        form = SponsorForm(
            user=self.user,
            project=self.project
        )
        self.assertFalse(form.is_valid())

        data = {
            'name': 'New Sponsor',
            'project': self.project.id
        }
        files = {
            'logo': SimpleUploadedFile(
                self.svg_content.name,
                self.svg_content.read()
            )
        }

        form = SponsorForm(
            data=data,
            files=files,
            user=self.user,
            project=self.project
        )
        self.assertTrue(form.is_valid())

    def test_upload_webp_file(self):
        form = SponsorForm(
            user=self.user,
            project=self.project
        )
        self.assertFalse(form.is_valid())

        data = {
            'name': 'New Sponsor',
            'project': self.project.id
        }
        files = {
            'logo': SimpleUploadedFile(
                self.webp_content.name,
                self.webp_content.read()
            )
        }

        form = SponsorForm(
            data=data,
            files=files,
            user=self.user,
            project=self.project
        )
        assert form.is_valid(), form.errors
