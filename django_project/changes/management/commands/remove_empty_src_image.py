# coding=utf-8
"""A command to fix the url image Entry. Issue #1304."""

from django.core.management.base import BaseCommand
from ...models import Entry


class Command(BaseCommand):
    """Remove img element with empty src value.
    """

    help = 'Remove img element with empty src value fetched from GitHub.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """Implementation for command.
        :param args:  Not used
        :param options: Not used
        """
        entries = Entry.objects.all()
        for entry in entries:
            if '<img  src="" />' in entry.description:
                description = entry.description.replace('<img  src="" />', '')
                entry.description = description
                entry.save(update_fields=['description'])
                self.stdout.write('Remove img element in %s' % entry.title)
        self.stdout.write(
            'Successfully remove all img element with empty src.')
