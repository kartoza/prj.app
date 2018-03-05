# coding=utf-8
"""Worksheet model definitions for lesson apps.

"""
import os
import logging

from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import override, get_language

from model_utils import FieldTracker

from lesson.models.section import Section
from lesson.utilities import custom_slug

logger = logging.getLogger(__name__)


class Worksheet(models.Model):
    """Worksheet lesson model."""

    tracker = FieldTracker()

    section = models.ForeignKey(Section)

    sequence_number = models.IntegerField(
        verbose_name=_('Worksheet number'),
        help_text=_(
            'The order in which this worksheet is listed within a section'),
        blank=False,
        null=False,
        default=0
    )

    module = models.CharField(
        help_text=_('Name of worksheet.'),
        blank=False,
        null=False,
        max_length=200,
    )

    title = models.CharField(
        help_text=_('Title of module.'),
        blank=False,
        null=False,
        max_length=200,
    )

    summary_leader = models.CharField(
        help_text=_('Title of the summary.'),
        blank=False,
        null=False,
        max_length=200,
    )

    summary_text = models.TextField(
        help_text=_('Content of the summary. Markdown is supported.'),
        blank=False,
        null=False,
        # max_length=1000, Not enough for now
    )

    summary_image = models.ImageField(
        help_text=_('Image of the summary. A landscape image, approximately '
                    '800*200. Most browsers support dragging the image '
                    'directly on to the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet/summary_image'),
        blank=True
    )

    exercise_goal = models.CharField(
        help_text=_('The goal of the exercise.'),
        blank=False,
        null=False,
        max_length=200,
    )

    exercise_task = models.TextField(
        help_text=_('Task in the exercise. Markdown is supported.'),
        blank=False,
        null=False,
        max_length=1000,
    )

    exercise_image = models.ImageField(
        help_text=_('Image for the exercise part. You should normally either '
                    'use the Requirements table or this image field. '
                    'A landscape image, approximately 800*200. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet/exercise'),
        blank=True
    )

    more_about_title = models.CharField(
        help_text=_('More about title.'),
        blank=False,
        null=False,
        max_length=200,
        default=_('More about'),
    )

    more_about_text = models.TextField(
        help_text=_(
            'More detail about the content of the worksheet. '
            'Markdown is supported.'),
        blank=False,
        null=False,
        # max_length=2000, Not enough for now
    )

    more_about_image = models.ImageField(
        help_text=_('Image for the more about part. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet/more_about'),
        blank=True
    )

    external_data = models.FileField(
        help_text=_('External data used in this worksheet. Usually a ZIP '
                    'file. Most browsers support dragging the file directly '
                    'on to the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet/external_data'),
        blank=True
    )
    youtube_link = models.URLField(
        help_text=_('Link to a YouTube video.'),
        null=True,
        blank=True
    )
    author_name = models.CharField(
        help_text=_('The author of this worksheet.'),
        blank=True,
        null=True,
        max_length=200,
    )
    author_link = models.URLField(
        help_text=_('Link to the author webpage.'),
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    last_update = models.DateTimeField(
        help_text=_('Time stamp when the last worksheet updated.'),
        blank=True,
        null=True
    )

    @property
    def is_translation_up_to_date(self):
        """Property to show if the translated version is up to date or not."""
        # Always up to date if the language is en.
        if get_language() == 'en':
            return True
        with override('en'):
            last_update_en = self.last_update
        # One of the last update is None, then translation is not up to date.
        if last_update_en is None or self.last_update is None:
            return False
        # Last update is older than English one --> no up to date.
        if self.last_update <= last_update_en:
            return False
        return True

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Worksheet model."""

        app_label = 'lesson'
        ordering = ['section', 'sequence_number']
        # Need to fix the transaction integrity after we submit a new order.
        # https://stackoverflow.com/questions/40891574/how-can-i-set-a-
        # table-constraint-deferrable-initially-deferred-in-django-model
        # unique_together = ['section', 'sequence_number']

    def save(self, *args, **kwargs):
        is_new_record = False if self.pk else True
        if is_new_record:
            # Default slug
            self.slug = custom_slug(self.module)

            # Section number
            max_number = Worksheet.objects.all().\
                filter(section=self.section).aggregate(
                models.Max('sequence_number'))
            max_number = max_number['sequence_number__max']
            # We take the maximum number. If the table is empty, we let the
            # default value defined in the field definitions.
            if max_number is not None:
                self.sequence_number = max_number + 1

        super(Worksheet, self).save(*args, **kwargs)

        if is_new_record:
            # We update the slug field with its ID and we save it again.
            self.slug = '{}-{}'.format(custom_slug(self.module), self.pk)[:50]
            self.save()

    def __unicode__(self):
        return self.module

from lesson.signals.worksheet import *  # noqa
