# coding=utf-8
"""Specification model definitions for lesson apps.

"""
import logging
from unidecode import unidecode

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from lesson.models.worksheet import Worksheet

from core.settings.contrib import STOP_WORDS

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

    slug = models.SlugField()

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for specification."""

        app_label = 'lesson'
        ordering = ['specification_number']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.title.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(Specification, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
