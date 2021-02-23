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
