# coding=utf-8
"""Specification model definitions for lesson apps.

"""
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lesson.models.worksheet import Worksheet

logger = logging.getLogger(__name__)


class Specification(models.Model):
    """Worksheet lesson model."""

    worksheet = models.ForeignKey(Worksheet)

    specification_number = models.IntegerField(
        help_text=_('Specification number.'),
    )

    title = models.CharField(
        help_text=_('Title of specification.'),
        max_length=200,
    )

    value = models.CharField(
        help_text=_('Value of specification.'),
        max_length=200,
    )

    notes = models.CharField(
        help_text=_('Notes of specification.'),
        max_length=200,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for specification."""

        app_label = 'lesson'
        ordering = ['specification_number']
        unique_together = ['specification_number', 'worksheet']

    def __unicode__(self):
        return self.title
