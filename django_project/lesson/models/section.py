# coding=utf-8
"""Section model definitions for lesson apps.

"""
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import FieldTracker

from lesson.models.mixins import TranslationMixin
from lesson.utilities import custom_slug

logger = logging.getLogger(__name__)


class Section(TranslationMixin):
    """Section lesson model.

    A section is a grouping for one or more lessons on a common theme
    e.g. digitising. Sections can be ordered so that the learner goes through
    the sections in the correct sequence.

    """

    tracker = FieldTracker()

    project = models.ForeignKey('base.Project',
                                on_delete=models.CASCADE,
                                verbose_name=_('Project name'))

    sequence_number = models.IntegerField(
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
        verbose_name=_('Section notes. Markdown is supported.'),
        help_text=_('Section notes.'),
        blank=False,
        null=False,
    )

    slug = models.SlugField(
        unique=True,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Section model."""

        app_label = 'lesson'
        ordering = ['project', 'sequence_number']
        # Need to fix the transaction integrity after we submit a new order.
        # https://stackoverflow.com/questions/40891574/how-can-i-set-a-
        # table-constraint-deferrable-initially-deferred-in-django-model
        # unique_together = ['project', 'sequence_number']

    def save(self, *args, **kwargs):
        is_new_record = False if self.pk else True
        if is_new_record:
            # Default slug
            self.slug = custom_slug(self.name)

            # Section number
            max_number = Section.objects.all().\
                filter(project=self.project).aggregate(
                models.Max('sequence_number'))
            max_number = max_number['sequence_number__max']
            # We take the maximum number. If the table is empty, we let the
            # default value defined in the field definitions.
            if max_number is not None:
                self.sequence_number = max_number + 1

        super(Section, self).save(*args, **kwargs)

        if is_new_record:
            # We update the slug field with its ID and we save it again.
            self.slug = '{}-{}'.format(custom_slug(self.name), self.pk)[:50]
            self.save()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


from lesson.signals.section import *  # noqa
