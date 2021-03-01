"""A command to remove unused media file"""

import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings

from changes.models.entry import Entry


def get_all_entries_images():
    """Get all images referenced by Entry instance

    There are images downloaded to Media, but not being referenced in
    ImageFile field instance. The images are referenced by hyperlink saved in
    description field.
    """

    all_media_size = 0
    github_image_size = 0
    image_field_size = 0

    # get images in images/entries
    upload_to = os.path.join(settings.MEDIA_ROOT, 'images/entries')

    all_media_images = []  # all images in images/entries
    for root, dirs, files in os.walk(upload_to):
        for name in files:
            path = os.path.abspath(os.path.join(root, name))
            # exclude thumbnails
            if re.match(r'^(?!.*/thumbnails/)', path):
                image_path = os.path.join(settings.MEDIA_ROOT, path)
                all_media_images.append(image_path)
                all_media_size += os.stat(image_path).st_size

    entries = Entry.objects.all()
    referenced_github_images = []  # image referenced in description
    image_field_images = []  # ImageField's image
    for entry in entries:
        if entry.image_file:
            image_path = os.path.join(
                settings.MEDIA_ROOT, entry.image_file.name
            )
            image_field_images.append(image_path)
            try:
                image_field_size += os.stat(image_path).st_size
            except FileNotFoundError:
                image_field_size += 0
                # scan image in entry description
        # result e.g images/entries/d4ede67e-fd0b-11e6-9de2.png
        images = re.findall(r'src=".*?(images/entries.*?)"', entry.description)
        # join path images
        # e.g /home/web/media/images/entries/d4ede67e-fd0b-11e6-9de2.png
        for image in images:
            path = os.path.join(settings.MEDIA_ROOT, image)
            referenced_github_images.append(path)
            try:
                github_image_size += os.stat(path).st_size
            except FileNotFoundError:
                github_image_size += 0
    return (
        referenced_github_images,
        image_field_images,
        all_media_images,
        github_image_size,
        image_field_size,
        all_media_size,
    )


class Command(BaseCommand):
    help = 'Remove all media that are not referenced by a valid project'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):

        # get Entry images
        (referenced_github_images,
         image_field_images,
         all_media_images,
         github_image_size,
         image_field_size,
         all_media_size) = get_all_entries_images()

        referenced_image = referenced_github_images + image_field_images
        unused_image = []
        unused_image_size = 0
        for image in all_media_images:
            if image not in referenced_image:
                unused_image.append(image)
                try:
                    unused_image_size += os.stat(image).st_size
                except FileNotFoundError:
                    unused_image_size += 0

        self.stdout.write('-' * 79)
        self.stdout.write(
            f'GitHub images: {len(referenced_github_images)} files, '
            f'ImageField images: {len(image_field_images)} files, and '
            f'All media images: {len(all_media_images)} files.'
        )
        self.stdout.write(
            f'GitHub images: {round(github_image_size/1000000, 2)} MB, '
            f'ImageField images: {round(image_field_size/1000000, 2)} MB, '
            f'All media images: {round(all_media_size/1000000, 2)} MB.'
        )

        confirmation = input(
            f'Do you want to delete unused Entry images '
            f'{len(unused_image)} files, '
            f'{round(unused_image_size/1000000, 2)} MB? [Y/n] '
        )

        if confirmation.lower() == 'y':
            self.stdout.write('remove files...')
            for image in unused_image:
                self.stdout.write(f'remove {image}')
                os.remove(image)
            self.stdout.write(
                'All unused Entry images have been removed successfully.'
            )
        else:
            self.stdout.write('remove files aborted!')
        exit()
