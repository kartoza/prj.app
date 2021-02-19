from io import StringIO
from django.core.management import call_command
from django.test import TestCase

from changes.tests.model_factories import EntryF


class FixUrlImageEntryTest(TestCase):
    def setUp(self):
        description = (
            '<p>There was no way we ship <em>QGIS 3.14 '
            '"Temporal edition"</em> without temporal support '
            'to layouts:<img  src="" /></p>'
        )
        self.entry = EntryF.create(description=description)
        self.entry.save()

    def test_command_output(self):
        out = StringIO()
        call_command('remove_empty_src_image', stdout=out)
        self.assertIn(
            'Remove img element in %s' % self.entry.title,
            out.getvalue())
