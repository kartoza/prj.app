# coding=utf-8
"""Worksheet question model definitions for lesson apps.

"""
import os
import logging

from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import FieldTracker

from lesson.models.mixins import TranslationMixin
from lesson.models.worksheet import Worksheet

logger = logging.getLogger(__name__)


class WorksheetQuestion(TranslationMixin):
    """Worksheet question lesson model.

    Question for checking participant's knowledge for each worksheet/module.
    """

    tracker = FieldTracker()

    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE)

    sequence_number = models.IntegerField(
        help_text=_(
            'Used to order the questions for a lesson into the correct '
            'sequence.'),
        null=False,
        blank=False,
        default=0
    )

    question = models.CharField(
        help_text=_('Question.'),
        blank=False,
        null=False,
        max_length=200,
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
        """Meta class for Worksheet Question model."""

        app_label = 'lesson'
        ordering = ['worksheet', 'sequence_number']
        # Need to fix the transaction integrity after we submit a new order.
        # https://stackoverflow.com/questions/40891574/how-can-i-set-a-
        # table-constraint-deferrable-initially-deferred-in-django-model
        # unique_together = ['worksheet', 'sequence_number']

    def save(self, *args, **kwargs):
        if not self.pk:
            # Question number
            max_number = WorksheetQuestion.objects.all().\
                filter(worksheet=self.worksheet).aggregate(
                models.Max('sequence_number'))
            max_number = max_number['sequence_number__max']
            # We take the maximum number. If the table is empty, we let the
            # default value defined in the field definitions.
            if max_number is not None:
                self.sequence_number = max_number + 1
        super(WorksheetQuestion, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.question


from lesson.signals.worksheet_question import *  # noqa
