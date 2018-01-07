# coding=utf-8
"""Section model definitions for lesson apps.

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

    module = models.CharField(
        help_text=_('Name of module.'),
        max_length=200,
    )

    title = models.CharField(
        help_text=_('Title of module.'),
        max_length=200,
    )

    summary_leader = models.CharField(
        help_text=_('Title of the summary.'),
        max_length=200,
    )

    summary_text = models.TextField(
        help_text=_('Content of the summary.'),
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
        max_length=200,
    )

    exercise_task = models.TextField(
        help_text=_('Task in the exercise.'),
        max_length=1000,
    )

    more_about_text = models.TextField(
        help_text=_('More detail about the content of the worksheet.'),
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

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Course attendee."""

        app_label = 'lesson'
        ordering = ['module']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.module.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(Worksheet, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.module
