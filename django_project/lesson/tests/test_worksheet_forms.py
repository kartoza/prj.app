from io import BytesIO
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from lesson.forms.worksheet import WorksheetForm

from base.tests.model_factories import ProjectF
from lesson.tests.model_factories import WorksheetF
from lesson.tests.model_factories import SectionF


class TestWorksheetForm(TestCase):

    def setUp(self) -> None:
        self.test_project = ProjectF.create()

        # Create section
        self.test_section = SectionF.create(project=self.test_project)
        self.test_worksheet = WorksheetF.create(section=self.test_section,
                                                published=True)
        dummy_file = BytesIO(b"some dummy bcode data: \x00\x01")
        dummy_file.name = 'test_file_name.zip'
        self.dummy_uploadedfile = SimpleUploadedFile(
            dummy_file.name, dummy_file.read())
        self.data = {
            'section': self.test_section.pk,
            'module': 'test module',
            'title': 'test title',
            'summary_leader': 'test summary',
            'summary_text': 'summary text',
        }

    def test_no_zipfile_clean_external_data_return_file(self):
        form = WorksheetForm(self.data, section=self.test_section)
        self.assertEqual(form.is_valid(), True)

    def test_not_valid_zipfile_clean_external_data_return_file(self):
        form = WorksheetForm(
            self.data,
            {'external_data': self.dummy_uploadedfile},
            section=self.test_section)
        self.assertEqual(form.is_valid(), False)

    @mock.patch('lesson.forms.worksheet.validate_zipfile', return_value=True)
    def test_valid_zipfile_clean_external_data_return_file(self, mock):
        form = WorksheetForm(
            self.data,
            {'external_data': self.dummy_uploadedfile},
            section=self.test_section)
        self.assertEqual(form.is_valid(), True)
