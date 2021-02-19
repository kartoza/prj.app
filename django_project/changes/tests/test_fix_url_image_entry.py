from io import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase

from changes.tests.model_factories import EntryF


class FixUrlImageEntryTest(TestCase):
    def setUp(self):
        gif_byte = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04'
            b'\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x44\x01\x00\x3b'
        )
        image_uploaded = SimpleUploadedFile(
            'gif.gif', gif_byte, content_type='image/gif')
        self.entry = EntryF.create(image_file=image_uploaded)
        old_path = self.entry.image_file.url
        self.entry.image_file = old_path
        self.entry.save()

    def test_command_output(self):
        self.assertIn('media/media', self.entry.image_file.url)
        out = StringIO()
        call_command('fix_url_image_entry', stdout=out)
        self.assertNotIn(
            'Replace url to media/media',
            out.getvalue())
