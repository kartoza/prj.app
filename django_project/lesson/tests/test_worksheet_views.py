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
        self.test_worksheet = WorksheetF.create(section=self.test_section,
                                                published=True)
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
        # Create zipfile in zipfile
        # inside zipfile : test_1.txt and test_inside_zip.zip
        # inside test_inside_zip.zip: test_inside_zip.txt
        zip_byte = (
            b'PK\x03\x04\x14\x00\x08\x00\x08\x00H]\xb1R\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x02\x00\x00\x00\n\x00 \x00test_1.txtUT\r\x00\x07'
            b'\x19\xe6\xa1`\x19\xe6\xa1`\x19\xe6\xa1`ux\x0b\x00\x01\x04\xe8'
            b'\x03\x00\x00\x04\xe8\x03\x00\x003\xe4\x02\x00PK\x07\x08S\xfcQg'
            b'\x04\x00\x00\x00\x02\x00\x00\x00PK\x03\x04\x14\x00\x08\x00\x08'
            b'\x00Y]\xb1R\x00\x00\x00\x00\x00\x00\x00\x00\xdc\x00\x00\x00\x13'
            b'\x00 \x00test_inside_zip.zipUT\r\x00\x07;\xe6\xa1`;\xe6\xa1`;'
            b'\xe6\xa1`ux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00'
            b'\x0b\xf0ff\x11a\xe0\x00\xc2\x90\xd8\x8dA\x0cP\xc0\x04\xc4\xc2'
            b'\x0c\n\x0c%\xa9\xc5%\xf1\x99y\xc5\x99)\xa9\xf1U\x99\x05z%\x15%'
            b'\xa1!\xbc\x0c\xec\x86\xcf\x16&\xc0pi\x057\x03#\xcb\x0bf\x06'
            b'\x060a\xfc\x88\x89!\xc0\x9b\x9dc\xc2\xfa\x1a\x1f\x16\xa8Q\x01'
            b'\xde\x8cL"\xcc\x08k\x90\xe5@\xd6\xc0\xc0\x96F\x10I\x86\xa5\x01'
            b'\xde\xacl \xad\x8c@\x98\x08\xa4S\xc1\xc6\x01\x00PK\x07\x08h\x06'
            b'\x07\x1as\x00\x00\x00\xdc\x00\x00\x00PK\x01\x02\x14\x03\x14\x00'
            b'\x08\x00\x08\x00H]\xb1RS\xfcQg\x04\x00\x00\x00\x02\x00\x00\x00'
            b'\n\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\xb4\x81\x00\x00\x00'
            b'\x00test_1.txtUT\r\x00\x07\x19\xe6\xa1`\x19\xe6\xa1`\x19\xe6'
            b'\xa1`ux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00'
            b'PK\x01\x02\x14\x03\x14\x00\x08\x00\x08\x00Y]\xb1Rh\x06\x07\x1as'
            b'\x00\x00\x00\xdc\x00\x00\x00\x13\x00 \x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\xb4\x81\\\x00\x00\x00test_inside_zip.zipUT\r\x00'
            b'\x07;\xe6\xa1`;\xe6\xa1`;\xe6\xa1`ux\x0b\x00\x01\x04\xe8\x03\x00'
            b'\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x02\x00\x02'
            b'\x00\xb9\x00\x00\x000\x01\x00\x00\x00\x00'
        )
        self.zip_uploaded = SimpleUploadedFile(
            'ziptest.zip', zip_byte, content_type='application/zip')

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
    def test_WorksheetDetailView_unpublished_worksheet_normal_view(self):
        """Tests accessing unpublish worksheet detail view in normal view."""

        self.test_worksheet.published = False
        self.test_worksheet.module = 'Unpublished worksheet'
        self.test_worksheet.save()
        response = self.client.get(reverse(
                'worksheet-detail', kwargs = self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 302)

        # Publish the worksheet
        self.test_worksheet.published = True
        self.test_worksheet.save()
        response = self.client.get(reverse(
                'worksheet-detail', kwargs = self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN = ['testserver', ])
    def test_WorksheetDetailView_unpublished_worksheet_admin_view(self):
        """Tests accessing unpublish worksheet detail view in admin view."""

        self.test_worksheet.published = False
        status = self.client.login(username='sonlinux', password='password')
        self.assertTrue(status)

        self.test_worksheet.module = 'Unpublished worksheet'
        self.test_worksheet.save()
        response = self.client.get(reverse(
                'worksheet-detail', kwargs = self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)

        # Publish the worksheet
        self.test_worksheet.published = True
        self.test_worksheet.save()
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
        self.assertContains(response, 'Select to change the section.')


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
    def WorksheetModuleQuestionAnswersPDF(self):
        """Test accessing module question answer"""

        self.test_project.name = 'Test Question Answer'
        self.test_project.save()
        self.test_worksheet.module = 'Test Module Question Answer'
        self.test_worksheet.save()
        response = self.client.get(reverse('worksheet-module-answers-print',
                                           kwargs=self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            'filename=Test Question Answer.pdf'
        )


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
            # ensure there's no zip inside zip
            for name in zip_file.namelist():
                self.assertFalse(name.endswith('.zip'))
            zip_file.close()


    @override_settings(VALID_DOMAIN=['testserver'])
    def test_WorksheetDownloadSampledataView(self):
        self.test_section.name = 'Test section zip'
        self.test_section.save()
        self.test_worksheet.summary_image = self.image_uploaded
        self.test_worksheet.more_about_image = self.image_uploaded
        self.test_worksheet.module = 'Test module zip'
        self.test_worksheet.save()

        response = self.client.get(reverse(
            'worksheet-sampledata', kwargs=self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 404)

        self.test_worksheet.external_data = self.zip_uploaded
        self.test_worksheet.save()
        response = self.client.get(reverse(
            'worksheet-sampledata', kwargs=self.kwargs_worksheet_full))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.get('Content-Disposition'),
            'attachment; filename=Test section zip-Test module zip.zip'
        )
        with io.BytesIO(response.content) as file:
            zip_file = zipfile.ZipFile(file, 'r')
            self.assertIsNone(zip_file.testzip())
            # zipfile must not contain any zipfile
            self.assertEqual(
                ['test_1.txt', 'test_inside_zip.txt'],
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
