# coding=utf-8
"""Section model definitions for lesson apps.

"""
import logging
from unidecode import unidecode

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from core.settings.contrib import STOP_WORDS

logger = logging.getLogger(__name__)


class Section(models.Model):
    """Section lesson model.

    A section is a grouping for one or more lessons on a common theme
    e.g. digitising. Sections can be ordered so that the learner goes through
    the sections in the correct sequence.

    """

    section_number = models.IntegerField(
        verbose_name=_('Section number'),
        help_text=_(
            'The order in which this section is listed within a project'),
        blank=False,
        null=False,
        default=0
    )

    name = models.CharField(
        verbose_name=_('Name of section'),
        help_text=_('Name of section.'),
        blank=False,
        null=False,
        max_length=200,
    )

    notes = models.TextField(
        verbose_name=_('Section notes.'),
        help_text=_('Section notes.'),
        blank=False,
        null=False,
        max_length=1000,
    )

    slug = models.SlugField()
    project = models.ForeignKey('base.Project', verbose_name=_('Project name'))

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Section model."""

        app_label = 'lesson'
        ordering = ['section_number']
        unique_together = ['slug', 'project']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(Section, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
