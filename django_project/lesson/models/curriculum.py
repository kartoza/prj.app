# coding=utf-8

"""Curriculum model definitions for lesson apps."""

import logging
import os

from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models.project import Project
from lesson.utilities import custom_slug

logger = logging.getLogger(__name__)


class Curriculum(models.Model):
    """Curriculum lesson model.

    A curriculum is a grouping for one or more worksheets owned by a user.
    """

    project = models.ForeignKey(
        Project,
        verbose_name=_('Project name'),
        help_text=_('The project.'),
        null=False,
        blank=False,
    )

    owner = models.ForeignKey(
        User,
        # default=get_default_organisation,
        help_text=_('The owner of the curriculum.'),
        null=False,
        blank=False,
    )

    title = models.CharField(
        verbose_name=_('Title of the curriculum'),
        help_text=_('Title of the curriculum.'),
        blank=False,
        null=False,
        max_length=200,
    )

    competency = models.CharField(
        verbose_name=_('Competency'),
        help_text=_('Competency.'),
        blank=True,
        null=True,
        max_length=200,
    )

    presenter_logo = models.ImageField(
        help_text=_(
            'Presenter logo. Most browsers support dragging the image '
            'directly on to the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/curriculum/presenter'),
        blank=True,
    )

    presenters = models.ManyToManyField(
        User,
        related_name='presenters',
        blank=True,
        # null=True, null has no effect on ManyToManyField.
        help_text=_(
            'Users who are presenting this curriculum.'),
    )

    slug = models.SlugField(
        unique=True,
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Section model."""

        app_label = 'lesson'
        ordering = ['project', 'title']
        # Need to fix the transaction integrity after we submit a new order.
        # https://stackoverflow.com/questions/40891574/how-can-i-set-a-
        # table-constraint-deferrable-initially-deferred-in-django-model
        # unique_together = ['project', 'sequence_number']

    def save(self, *args, **kwargs):
        is_new_record = False if self.pk else True
        if is_new_record:
            # Default slug
            self.slug = custom_slug(self.title)

        super(Curriculum, self).save(*args, **kwargs)

        if is_new_record:
            # We update the slug field with its ID and we save it again.
            self.slug = '{}-{}'.format(custom_slug(self.title), self.pk)[:50]
            self.save()

    def __unicode__(self):
        return self.title
