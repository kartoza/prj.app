# coding=utf-8
"""Specification model definitions for lesson apps.

"""
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import FieldTracker

from lesson.models.mixins import TranslationMixin
from lesson.models.worksheet import Worksheet


logger = logging.getLogger(__name__)


class Specification(TranslationMixin):
    """Specification lesson model.

    A specification is a particular requirement for a task that the learner
    is required to do in the lesson.
    """

    tracker = FieldTracker()

    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE)

    sequence_number = models.IntegerField(
        help_text=_(
            'Used to order the specifications for a lesson into the correct '
            'sequence.'),
        blank=False,
        null=False,
        default=0
    )

    title = models.CharField(
        help_text=_('Title of specification. Markdown is supported'),
        blank=False,
        null=False,
        max_length=200,
    )

    value = models.CharField(
        help_text=_('Value of specification. Markdown is supported'),
        blank=False,
        null=False,
        max_length=200,
    )

    title_notes = models.CharField(
        help_text=_('Description of title field. Markdown is supported'),
        blank=True,
        null=True,
        max_length=200,
    )

    value_notes = models.CharField(
        help_text=_('Description of value field. Markdown is supported'),
        blank=True,
        null=True,
        max_length=200,
    )

    # noinspection PyClassicStyleClass.
    class Meta:

        """Meta class for specification."""

        app_label = 'lesson'
        ordering = ['worksheet', 'sequence_number']
        # Need to fix the transaction integrity after we submit a new order.
        # https://stackoverflow.com/questions/40891574/how-can-i-set-a-
        # table-constraint-deferrable-initially-deferred-in-django-model
        # unique_together = ['worksheet', 'sequence_number']

    def save(self, *args, **kwargs):
        if not self.pk:
            # Specification number
            max_number = Specification.objects.all(). \
                filter(worksheet=self.worksheet).aggregate(
                models.Max('sequence_number'))
            max_number = max_number['sequence_number__max']
            # We take the maximum number. If the table is empty, we let the
            # default value defined in  the field definitions.
            if max_number is not None:
                self.sequence_number = max_number + 1

        super(Specification, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


from lesson.signals.specification import *  # noqa
