# coding=utf-8
"""Worksheet model definitions for lesson apps.

"""
import os
import logging
from unidecode import unidecode

from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from core.settings.contrib import STOP_WORDS

from lesson.models.section import Section

logger = logging.getLogger(__name__)


class Worksheet(models.Model):
    """Worksheet lesson model."""

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
        help_text=_('Content of the summary.'),
        blank=False,
        null=False,
        max_length=1000,
    )

    summary_image = models.ImageField(
        help_text=_('Image of the summary. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
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
        help_text=_('Task in the exercise.'),
        blank=False,
        null=False,
        max_length=1000,
    )

    more_about_title = models.TextField(
        help_text=_('More about title.'),
        blank=False,
        null=False,
        max_length=200,
        default=_('More about'),
    )

    more_about_text = models.TextField(
        help_text=_('More detail about the content of the worksheet.'),
        blank=False,
        null=False,
        max_length=2000,
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

    slug = models.SlugField()

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Worksheet model."""

        app_label = 'lesson'
        ordering = ['section', 'sequence_number']
        unique_together = ['section', 'sequence_number']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.module.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

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

    def __unicode__(self):
        return self.module
