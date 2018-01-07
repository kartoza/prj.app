# coding=utf-8
"""Answer model definitions for lesson apps.

"""
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lesson.models.worksheet_question import WorksheetQuestion, Worksheet
logger = logging.getLogger(__name__)


class Answer(models.Model):
    """Answer lesson model."""

    question = models.ForeignKey(WorksheetQuestion)

    answer_number = models.IntegerField(
        help_text=_('Answer number.'),
    )

    is_correct = models.BooleanField(
        help_text=_('Is this answer correct?'),
    )

    answer = models.CharField(
        help_text=_('Answer.'),
        max_length=200,
    )

    answer_explanation = models.TextField(
        help_text=_('Answer explanation.'),
        max_length=1000,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Answer."""

        app_label = 'lesson'
        unique_together = [
            'answer_number', 'question']

    def __unicode__(self):
        return self.answer
