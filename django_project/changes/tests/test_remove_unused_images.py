from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from changes.management.commands.remove_unused_images import (
    get_ImageField_and_ImageField,
    get_meta_of_models_media,
    get_all_Entry_images,
    get_all_media,
    get_unused_media,
)
from base.tests.model_factories import ProjectF
from changes.tests.model_factories import (
    CategoryF,
    VersionF)
from core.model_factories import UserF
from changes.models import Entry


class TestGetAllEntriesImage(TestCase):
    def setUp(self) -> None:
        gif_byte = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04'
            b'\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x44\x01\x00\x3b'
        )
        image_uploaded = SimpleUploadedFile(
            'gif.gif', gif_byte, content_type='image/gif')
        self.project = ProjectF.create()
        self.category = CategoryF.create(project=self.project)
        self.version = VersionF.create(project=self.project)
        self.user = UserF.create(**{
            'username': 'suman',
            'password': 'password',
            'is_staff': True
        })
        self.entry = Entry.objects.create(
            version=self.version,
            category=self.category,
            author=self.user,
            title='Test remove unused images.',
            image_file=image_uploaded,
            description=(
                '<h2>Description</h2><p><img  '
                'src="/media/images/entries/75693398-2ba8d480-5ca7-11ea-8be0-'
                '9643f8841c89-2.png" /><img  src="/media/images/entries/'
                '75693404-2d729800-5ca7-11ea-889d-5aa73bc131ce-1.png" /></p>')
        )

    def test_get_ImageField_and_ImageField(self):
        model = get_ImageField_and_ImageField(Entry)
        self.assertIn('changes', model[0])
        self.assertIn('Entry', model[0])
        self.assertIn('image_file', model[0])
        self.assertIn('images/entries', model[0])

    def test_get_meta_of_models_media(self):
        models = get_meta_of_models_media()
        self.assertTrue(len(models) > 0)
        self.assertIn(
            ('base', 'Project', 'image_file', 'images/projects'), models
        )

    def test_get_all_Entry_images(self):
        (referenced_github_images,
            image_field_images,
            all_media_images,
            github_image_size,
            image_field_size,
            all_media_size) = get_all_Entry_images()
        self.assertTrue(len(all_media_images) > 0)
        self.assertTrue(all_media_size >= image_field_size)
        self.assertTrue(all_media_size >= github_image_size)

    def test_get_all_media(self):
        (image_and_file_files,
            image_and_file_size,
            all_media_files,
            all_media_size) = get_all_media()
        self.assertTrue(len(all_media_files) > 0)
        self.assertTrue(all_media_size >= image_and_file_size)

    def test_get_unused_media_Entry(self):
        (all_media,
         unused_media,
         all_media_size,
         unused_media_size) = get_unused_media(is_Entry=True)

        self.assertTrue(all_media_size > unused_media_size)
        self.assertTrue(len(all_media) > len(unused_media))

    def test_get_unused_media_exclude_Entry(self):
        (all_media,
         unused_media,
         all_media_size,
         unused_media_size) = get_unused_media(is_Entry=False)

        self.assertTrue(all_media_size > unused_media_size)
        self.assertTrue(len(all_media) > len(unused_media))

    @patch('changes.management.commands.remove_unused_images.get_input',
           return_value='n')
    @patch('changes.management.commands.remove_unused_images.os.remove')
    def test_command_output_no(self, mocked_remove, mock_user_input):
        out = StringIO()
        call_command('remove_unused_images', stdout=out)
        self.assertEqual(mock_user_input.called, True)

        (text,), kwargs = mock_user_input.call_args
        self.assertIn('Delete unused media images and files:', text)
        self.assertFalse(mocked_remove.called)

    @patch('changes.management.commands.remove_unused_images.get_input',
           return_value='Y')
    @patch('changes.management.commands.remove_unused_images.os.remove')
    def test_command_output_yes(self, mocked_remove, mock_user_input):
        out = StringIO()
        call_command('remove_unused_images', stdout=out)
        self.assertEqual(mock_user_input.called, True)

        self.assertIn(
            'All unused Entry images have been removed successfully.',
            out.getvalue())
        self.assertTrue(mocked_remove.called)
