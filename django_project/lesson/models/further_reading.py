# coding=utf-8
"""Further reading model definitions for lesson apps.

"""
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lesson.models.worksheet import Worksheet

logger = logging.getLogger(__name__)


class FurtherReading(models.Model):
    """Further reading lesson model."""

    worksheet = models.ForeignKey(Worksheet)

    text = models.CharField(
        help_text=_('Text of the further reading.'),
        max_length=200,
    )

    link = models.CharField(
        help_text=_('Link of the further reading.'),
        max_length=200,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Course attendee."""

        app_label = 'lesson'

    def __unicode__(self):
        return self.text
