# coding=utf-8
"""Section model definitions for lesson apps.

"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode
from core.settings.contrib import STOP_WORDS
from django.utils.text import slugify
import logging
logger = logging.getLogger(__name__)


class Section(models.Model):
    """Section lesson model."""

    section_number = models.IntegerField(
        help_text=_('Section number.'),
    )

    name = models.CharField(
        help_text=_('Name of lesson.'),
        max_length=200,
    )

    notes = models.TextField(
        help_text=_('Name of lesson.'),
        max_length=1000,
    )

    slug = models.SlugField()
    project = models.ForeignKey('base.Project')

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Section."""

        app_label = 'lesson'
        ordering = ['section_number']
        unique_together = ['section_number', 'project']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = \
                self.project.slug + ' ' + \
                unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(Section, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
