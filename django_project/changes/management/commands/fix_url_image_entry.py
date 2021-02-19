# coding=utf-8
"""A command to fix the url image Entry. Issue #1305."""

from django.core.management.base import BaseCommand
from ...models import Entry


class Command(BaseCommand):
    """Update all Entry image_file that has an incorrect fetched from GitHub.
    """

    help = 'Fix url image_file fetched from GitHub.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """Implementation for command.
        :param args:  Not used
        :param options: Not used
        """
        entries = Entry.objects.all()
        for entry in entries:
            # replace 'media/images/entries' to 'images/entries'
            image_file = entry.image_file
            if image_file:
                if 'media/media/images/entries' in image_file.url:
                    self.stdout.write('Fix %s in %s' % (
                        image_file.url, entry.title))
                    image_path = image_file.url.replace(
                        '/media/media/images/entries',
                        'images/entries'
                    )
                    entry.image_file = image_path
                    entry.save(update_fields=['image_file'])
                    self.stdout.write(
                        'Replace url to %s' % entry.image_file.url
                    )

        self.stdout.write('Successfully updated all entry images.')
