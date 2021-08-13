"""A command to remove unused media file"""

import os
import re
from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings

from changes.models.entry import Entry


def get_ImageField_and_ImageField(model):
    result = []
    for field in model._meta.fields:
        if (field.get_internal_type() == 'ImageField' or
                field.get_internal_type() == 'FileField'):
            result.append((
                model._meta.app_label,
                model.__name__,
                field.name,
                field.upload_to
            ))
    return result


def get_meta_of_models_media():
    """Get list of all models in app"""

    app_models = [model for model in apps.get_models()]

    # get models which has ImageField or FileField fields
    media_fields = []
    for model in app_models:
        media_fields.extend(get_ImageField_and_ImageField(model))
    return media_fields


def get_all_media():
    """Scan all unused media
    """

    image_and_file_files = []  # ImageField and FileField files
    image_and_file_size = 0  # ImageField and FileField filesize

    all_media_files = []
    all_media_size = 0
    media_fields = get_meta_of_models_media()
    for media in media_fields:
        app_label, model_name, field_name, upload_to = media
        # exclude Entry models instance
        # it's handled in another function
        if model_name == 'Entry':
            continue
        for root, dirs, files in os.walk(os.path.join(
                settings.MEDIA_ROOT, upload_to)):
            for name in files:
                path = os.path.abspath(os.path.join(root, name))
                # exclude thumbnails
                if re.match(r'^(?!.*/thumbnails/)', path):
                    image_path = os.path.join(settings.MEDIA_ROOT, path)
                    all_media_files.append(image_path)
                    all_media_size += os.stat(image_path).st_size

        model = apps.get_model(app_label, model_name)  # e.g Worksheet
        objects = model.objects.all()
        for obj in objects:
            # get field
            field_object = model._meta.get_field(field_name)  # e.g image_file
            # get field value
            field_value = field_object.value_from_object(obj)
            if field_value:
                file_path = os.path.join(
                    settings.MEDIA_ROOT, field_value.name
                )
                image_and_file_files.append(file_path)
                try:
                    image_and_file_size += os.stat(file_path).st_size
                except FileNotFoundError:
                    image_and_file_size += 0

    return (
        image_and_file_files,
        image_and_file_size,
        all_media_files,
        all_media_size,
    )


def get_all_Entry_images():
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


def get_unused_media(is_Entry=False):
    all_media = []
    unused_media = []

    all_media_size = 0
    unused_media_size = 0

    if is_Entry:
        # Entry media instances
        (referenced_github_images,
         entry_image_field_images,
         entry_all_media_images,
         github_image_size,
         entry_image_field_size,
         entry_all_media_size) = get_all_Entry_images()

        referenced_image = referenced_github_images + entry_image_field_images
        for image in entry_all_media_images:
            if image not in referenced_image:
                unused_media.append(image)
                try:
                    unused_media_size += os.stat(image).st_size
                except FileNotFoundError:
                    unused_media_size += 0

        all_media = entry_all_media_images
        all_media_size = entry_all_media_size

        return (all_media, unused_media, all_media_size, unused_media_size)

    # another
    (image_and_file_files,
     image_and_file_size,
     all_media_files,
     all_media_size) = get_all_media()

    for media in all_media_files:
        if media not in image_and_file_files:
            unused_media.append(media)
            try:
                unused_media_size += os.stat(media).st_size
            except FileNotFoundError:
                unused_media_size += 0

    all_media = all_media_files

    return (all_media, unused_media, all_media_size, unused_media_size)


def get_input(text):
    return input(text)


class Command(BaseCommand):
    help = 'Remove all media that are not referenced by a valid project'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):

        # get all media exclude Entry
        (all_media,
         unused_media,
         all_media_size,
         unused_media_size) = get_unused_media()


        # get Entry images
        (all_entries_media,
         unused_entries_media,
         all_entries_size,
         unused_entries_size) = get_unused_media(is_Entry=True)

        self.stdout.write('=' * 79)
        self.stdout.write('Entry\'s Media')
        self.stdout.write('-' * 30)
        self.stdout.write(
            f'All Entry media : {len(all_entries_media)} files '
            f'{round(all_entries_size / 1000000, 2)} MB.\n'
            f'Unused Entry media : {len(unused_entries_media)} files '
            f'{round(unused_entries_size / 1000000, 2)} MB.'
        )
        self.stdout.write('\n')
        self.stdout.write('All Media (exclude Entry model instance)')
        self.stdout.write('-' * 30)
        self.stdout.write(
            f'All Entry media : {len(all_media)} files '
            f'{round(all_media_size / 1000000, 2)} MB.\n'
            f'Unused Entry media : {len(unused_media)} files '
            f'{round(unused_media_size / 1000000, 2)} MB.'
        )

        confirmation = get_input(
            f'\nDelete unused media images and files: '
            f'{len(unused_entries_media) + len(unused_media)} files, '
            f'{round((unused_entries_size + unused_media_size)/1000000, 2)} '
            f'MB? [Y] '
        )

        if confirmation.lower() == 'y':
            self.stdout.write('remove files...')
            for image in unused_entries_media:
                self.stdout.write(f'remove {image}')
                try:
                    os.remove(image)
                except FileNotFoundError:
                    continue
            for image in unused_media:
                self.stdout.write(f'remove {image}')
                try:
                    os.remove(image)
                except FileNotFoundError:
                    continue
            self.stdout.write(
                'All unused Entry images have been removed successfully.'
            )
        else:
            self.stdout.write('remove files aborted!')
