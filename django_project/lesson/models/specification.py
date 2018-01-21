# coding=utf-8
"""Specification model definitions for lesson apps.

"""
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lesson.models.worksheet import Worksheet


logger = logging.getLogger(__name__)


class Specification(models.Model):
    """Specification lesson model.

    A specification is a particular requirement for a task that the learner
    is required to do in the lesson.
    """

    worksheet = models.ForeignKey(Worksheet)

    specification_number = models.IntegerField(
        help_text=_(
            'Used to order the specifications for a lesson into the correct '
            'sequence.'),
        blank=False,
        null=False,
        default=0
    )

    title = models.CharField(
        help_text=_('Title of specification.'),
        blank=False,
        null=False,
        max_length=200,
    )

    value = models.CharField(
        help_text=_('Value of specification.'),
        blank=False,
        null=False,
        max_length=200,
    )

    notes = models.CharField(
        help_text=_('Notes of specification.'),
        blank=True,
        null=False,
        max_length=200,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for specification."""

        app_label = 'lesson'
        ordering = ['specification_number']

    def __unicode__(self):
        return self.title
