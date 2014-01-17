# coding=utf-8
"""A command to get rid of any images that are not being actively used."""
from django.core.management.base import BaseCommand
from django.core.files import File
from ...models import Entry


class Command(BaseCommand):
    """Update all images to their hashed equivalents and remove unused images.
    """
    args = ''
    # noinspection PyShadowingBuiltins
    help = 'Removes all unused images from the media folder.'

    def handle(self, *args, **options):
        """Implementation for command.
        :param args:  Not used
        :param options: Not used
        """
        entries = Entry.all_objects.all()
        for entry in entries:
            # Force converting image to a hashed name
            # this is to support image migrations of older versions
            # of changelogger.

            self.stdout.write(entry.title)
            image_path = entry.image_file.name
            if 'images/entries' in image_path:
                self.stdout.write('Skipping %s' % image_path)
                continue
            else:
                self.stdout.write('Moving %s' % image_path)
            image_file = File(image_path)
            entry.image_file.save(image_path, image_file, True)
            #os.remove(image_path)

        # except Exception, e:
        #     raise CommandError(e.message)

        self.stdout.write('Successfully updated all entry images.')
