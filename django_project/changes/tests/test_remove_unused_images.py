from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from changes.management.commands.remove_unused_images import \
    get_all_entries_images
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

    def test_get_all_entries_images(self):
        (referenced_github_images,
         image_field_images,
         all_media_images,
         github_image_size,
         image_field_size,
         all_media_size) = get_all_entries_images()

        self.assertEqual(len(referenced_github_images), 2)
        self.assertEqual(len(image_field_images), 1)
