# coding=utf-8
"""Further reading model definitions for lesson apps.

"""
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import FieldTracker

from lesson.models.mixins import TranslationMixin
from lesson.models.worksheet import Worksheet

logger = logging.getLogger(__name__)


class FurtherReading(TranslationMixin):
    """Further reading lesson model.

    This is a forward link for the topic so that the lesson reader can find
    more info about the topic.
    """

    tracker = FieldTracker()

    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE)

    text = models.TextField(
        help_text=_('Text of the further reading.'),
        blank=False,
        null=False,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Further Reading model."""

        app_label = 'lesson'
        ordering = ['worksheet']

    def __unicode__(self):
        return self.text


from lesson.signals.further_reading import *  # noqa
