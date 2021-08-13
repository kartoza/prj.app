<<<<<<< HEAD
from unittest import mock

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from lesson.utilities import validate_zipfile


class TestZipfileValidation(SimpleTestCase):

    def test_validate_zipfile_valid(self):
        with mock.patch('lesson.utilities.zipfile.ZipFile') as mock_ZipFile:
            mock_ZipFile.return_value.namelist.return_value = ('file.py',)
            validation = validate_zipfile(mock_ZipFile)
            self.assertTrue(validation)

    def test_validate_zipfile_include_git(self):
        with mock.patch('lesson.utilities.zipfile.ZipFile') as mock_ZipFile:
            mock_ZipFile.return_value.namelist.return_value = (
                'file.py', '.git'
            )
            self.assertRaises(ValidationError, validate_zipfile, mock_ZipFile)

    def test_validate_zipfile_include_macOSX(self):
        with mock.patch('lesson.utilities.zipfile.ZipFile') as mock_ZipFile:
            mock_ZipFile.return_value.namelist.return_value = (
                'file.py', '__MACOSX'
            )
            self.assertRaises(ValidationError, validate_zipfile, mock_ZipFile)

    def test_validate_zipfile_include_pycache(self):
        with mock.patch('lesson.utilities.zipfile.ZipFile') as mock_ZipFile:
            mock_ZipFile.return_value.namelist.return_value = (
                'file.py', '__pycache__'
            )
            self.assertRaises(ValidationError, validate_zipfile, mock_ZipFile)
=======
# coding=utf-8
"""Test for lesson utilities."""

from django.test import TestCase

from lesson.tests.model_factories import (FurtherReadingF,
                                          SectionF,
                                          WorksheetF)
from base.tests.model_factories import ProjectF

from lesson.utilities import GetAllFurtherReadingLink


class AllFurtherReadingURL(TestCase):

    def setUp(self):
        # Create project
        self.test_project = ProjectF.create(
            name = 'Test project'
        )

        # Create section
        self.test_section = SectionF.create(
            project=self.test_project,
            name='Test section'
        )
        self.test_worksheet = WorksheetF.create(
            section=self.test_section,
            published=True,
            module='Test Invalid Link'
        )
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
        self.test_further_reading = FurtherReadingF.create(
            worksheet=self.test_worksheet)

    def test_get_all_url_list(self):
        self.test_further_reading.text = (
            'Test for link: <a href="https://changelog.kartoza.com/en/">'
            'https://changelog.kartoza.com/en/</a> and '
            '<a href="https://changelog.qgis.org/en/qgis/lessons/'
            '#introduction-qgis-1">link</a>. But this one won\'t included')
        self.test_further_reading.save()
        obj = GetAllFurtherReadingLink(self.test_project)
        result = obj.get_url_list(self.test_further_reading.text)
        self.assertEqual(
            result,
            ['https://changelog.kartoza.com/en/',
             'https://changelog.qgis.org/en/qgis/lessons/#introduction-qgis-1'
             ], msg=result
        )
>>>>>>> 58aec98309b3aa1ca18b9c776e5b9bac2a086126
