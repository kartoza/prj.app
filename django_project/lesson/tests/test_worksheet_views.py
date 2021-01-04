# coding: utf-8
"""Unit tests for worksheet views."""

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__copyright__ = 'kartoza.com'


import io
import logging
import zipfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings, Client
from django.urls import reverse

from lesson.tests.model_factories import WorksheetF
from lesson.tests.model_factories import SectionF
from lesson.tests.model_factories import LicenseF
from base.tests.model_factories import ProjectF
from core.model_factories import UserF


class TestViews(TestCase):
    """Tests that Lesson Section views work."""

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def setUp(self):
        """
        Setup before each test
        We force the locale to en otherwise it will use
        the locale of the host running the tests and we
        will get unpredictable results / 404s
        """

        self.client = Client()
        self.client.post(
                '/set_language/', data = {'language': 'en'})
        logging.disable(logging.CRITICAL)
        self.user = UserF.create(
            **{'username': 'sonlinux', 'is_staff': True})
        # Something changed in the way factoryboy works with django 1.8
        # I think - we need to explicitly set the users password
        # because the core.model_factories.UserF._prepare method
        # which sets the password is never called. Next two lines are
        # a work around for that - sett #581
        self.user.set_password('password')
        self.user.save()

        # Create project
        self.test_project = ProjectF.create()

        # Create section
        self.test_section = SectionF.create(project=self.test_project)
        self.test_worksheet = WorksheetF.create(section=self.test_section)
        self.kwargs_project = {'project_slug': self.test_section.project.slug}
        self.kwargs_section = {'slug': self.test_section.slug}
        self.kwargs_section_full = {
            'project_slug': self.test_section.project.slug,
            'slug': self.test_section.slug
        }
        self.kwargs_worksheet_full = {
            'project_slug': self.test_section.project.slug,
            'section_slug': self.test_section.slug,
            'pk': self.test_worksheet.pk
        }
        # Create license
        self.license = LicenseF.create()
        gif_byte = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04'
            b'\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x44\x01\x00\x3b'
        )
        self.image_uploaded = SimpleUploadedFile(
            'gif.gif', gif_byte, content_type='image/gif')

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetCreateView(self):
        """Test accessing worksheet create view with no login."""

        post_data = {
            'module': u'Demo worksheet name',
            'title': u'Demo worksheet title',
            'section': self.test_section.id,
        }
        response = self.client.post(
                reverse('worksheet-create', kwargs = {
                    'project_slug': self.test_section.project.slug,
                    'section_slug': self.test_section.slug}),
                post_data)
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetCreateView_with_login(self):
        """Test accessing worksheet create view with login."""

        status = self.client.login(username='sonlinux', password='password')
        self.assertTrue(status)
        post_data = {
            'module': u'Demo worksheet name',
            'title': u'Demo worksheet title',
            'section': self.test_section.id,
        }
        response = self.client.post(
                reverse('worksheet-create', kwargs = {
                    'project_slug': self.test_section.project.slug,
                    'section_slug': self.test_section.slug}),
                post_data)

        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetDetailView(self):
        """Tests accessing worksheet detail view."""

        response = self.client.get(reverse(
                'worksheet-detail', kwargs = self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetUpdateView(self):
        """Tests updating worksheet without login."""

        response = self.client.get(reverse(
                'worksheet-update', kwargs = self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 302)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetUpdateView_with_login(self):
        """Tests updating worksheet with login."""

        status = self.client.login(username='sonlinux', password='password')
        self.assertTrue(status)
        response = self.client.get(reverse(
            'worksheet-update', kwargs=self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'update.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_WorksheetModuleQuestionAnswers(self):
        """Test accessing module question answer"""

        self.test_project.name = 'Test Question Answer'
        self.test_project.save()
        self.test_worksheet.module = 'Test Module Question Answer'
        self.test_worksheet.save()
        response = self.client.get(reverse('worksheet-module-answers',
                                           kwargs=self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Question Answer')
        self.assertContains(response, 'Test Module Question Answer')

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_WorksheetPrintView(self):
        self.test_section.name = 'Test section print'
        self.test_section.save()
        self.test_worksheet.summary_image = self.image_uploaded
        self.test_worksheet.more_about_image = self.image_uploaded
        self.test_worksheet.module = 'Test module print'
        self.test_worksheet.save()
        response = self.client.get(reverse(
            'worksheet-print', kwargs= self.kwargs_worksheet_full
        ) + '?q=1')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            'filename=1. Test section print-Test module print.pdf'
        )

    @override_settings(VALID_DOMAIN=['testserver'])
    def test_WorksheetPDFZipView(self):
        self.test_section.name = 'Test section zip'
        self.test_section.save()
        self.test_worksheet.summary_image = self.image_uploaded
        self.test_worksheet.more_about_image = self.image_uploaded
        self.test_worksheet.module = 'Test module zip'
        self.test_worksheet.license = self.license
        self.test_worksheet.save()
        response = self.client.get(reverse(
            'worksheet-zip', kwargs=self.kwargs_worksheet_full
        ) + '?q=2')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            'attachment; filename=2. Test section zip-Test module zip.zip'
        )
        with io.BytesIO(response.content) as file:
            zip_file = zipfile.ZipFile(file, 'r')
            self.assertIsNone(zip_file.testzip())
            self.assertIn('2. Test section zip-Test module zip/license.txt',
                          zip_file.namelist())
            zip_file.close()


    @override_settings(VALID_DOMAIN=['testserver'])
    def test_download_multiple_worksheets(self):
        self.test_project.name = 'Test project name multiple zip'
        self.test_project.save()
        self.test_section.name = 'Section Multiple Download'
        self.test_section.save()
        self.test_worksheet.summary_image = self.image_uploaded
        self.test_worksheet.more_about_image = self.image_uploaded
        self.test_worksheet.license = self.license
        self.test_worksheet.save()
        worksheet_obj = ('?worksheet={%22' +
                         str(self.test_worksheet.pk) +
                         '%22:%221.1%22}')
        response = self.client.get(reverse(
            'download-multiple-worksheets', kwargs=self.kwargs_project
        ) + worksheet_obj)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            'attachment; '
            'filename=Test project name multiple zip-worksheet module 1.1.zip'
        )
        with io.BytesIO(response.content) as file:
            zip_file = zipfile.ZipFile(file, 'r')
            self.assertIsNone(zip_file.testzip())
            self.assertIn('1. Section Multiple Download/Test License.txt',
                          zip_file.namelist())
            zip_file.close()
