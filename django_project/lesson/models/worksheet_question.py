# coding=utf-8
"""Worksheet question model definitions for lesson apps.

"""
import os
import logging

from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lesson.models.worksheet import Worksheet

logger = logging.getLogger(__name__)


class WorksheetQuestion(models.Model):
    """Worksheet question lesson model."""

    worksheet = models.ForeignKey(Worksheet)

    question = models.CharField(
        help_text=_('Question.'),
        max_length=200,
        blank=False
    )

    question_number = models.IntegerField(
        help_text=_('Question number.'),
        null=False,
        blank=False,
    )

    question_image = models.ImageField(
        help_text=_('Image for the question. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet_question/question_image'),
        blank=True
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Worksheet Question."""

        app_label = 'lesson'
        ordering = ['question_number', 'worksheet']
        unique_together = ['question_number', 'question']

    def __unicode__(self):
        return self.question
