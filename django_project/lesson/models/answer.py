# coding=utf-8
"""Answer model definitions for lesson apps.

"""
import logging

from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _

from lesson.models.worksheet_question import WorksheetQuestion

logger = logging.getLogger(__name__)


class Answer(models.Model):
    """Answer lesson model.

    Each lesson can have zero or more questions associated with it. The
    question will have one or more answers and the answer will have an
    indication if it is a correct answer or not. One question could have
    more than one correct answers (or no correct answers).
    """

    question = models.ForeignKey(WorksheetQuestion)

    answer_number = models.IntegerField(
        help_text=_(
            'Used to order the answers for a question into the correct '
            'sequence.'),
        blank=False,
        null=False,
        default=0,
    )

    is_correct = models.BooleanField(
        help_text=_('Is this answer correct?'),
        blank=False,
        null=False,
    )

    answer = models.CharField(
        help_text=_('Answer.'),
        blank=False,
        null=False,
        max_length=200,
    )

    answer_explanation = models.TextField(
        help_text=_('Answer explanation.'),
        blank=True,
        null=False,
        max_length=1000,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Answer module."""

        app_label = 'lesson'
        unique_together = ['answer_number', 'question']

    def save(self, *args, **kwargs):
        if not self.pk:
            max_answer_number = Answer.objects.all().\
                filter(question=self.question).aggregate(Max('answer_number'))
            self.answer_number = max_answer_number['answer_number__max'] + 1
        super(Answer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.answer
