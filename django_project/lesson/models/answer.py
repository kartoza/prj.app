# coding=utf-8
"""Answer model definitions for lesson apps.

"""
import logging

from django.db import models
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

    sequence_number = models.IntegerField(
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
        help_text=_('Answer explanation. Markdown is supported.'),
        blank=True,
        null=False,
        max_length=1000,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Answer module."""

        app_label = 'lesson'
        unique_together = ['question', 'sequence_number']
        ordering = ['question', 'sequence_number']

    def save(self, *args, **kwargs):
        if not self.pk:
            # Answer number
            max_number = Answer.objects.all().\
                filter(question=self.question).aggregate(
                models.Max('sequence_number'))
            max_number = max_number['sequence_number__max']
            # We take the maximum number. If the table is empty, we let the
            # default value defined in the field definitions.
            if max_number is not None:
                self.sequence_number = max_number + 1

        super(Answer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.answer
