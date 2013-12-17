# coding=utf-8
"""
This model is used to create 'committees' of users.

A Committee has many Users
"""
from django.core.urlresolvers import reverse
from django.utils.text import slugify

import logging
logger = logging.getLogger(__name__)
from django.db import models
from audited_models.models import AuditedModel
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

QUORUM_CHOICES = (
    ('100', 'All Members'),
    ('75', 'Three Quarters'),
    ('50', 'Half'),
    ('25', 'One Quarter'),
    ('1', 'One Member')
)


class Committee(AuditedModel):
    """A committee model i.e. a group of users under a project"""
    name = models.CharField(
        help_text=_('The name of this committee.'),
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    description = models.TextField(
        help_text=_('A description of the committee\'s role within the '
                    'project.'),
        max_length=1000,
        null=True,
        blank=True,
    )

    sort_number = models.SmallIntegerField(
        help_text=_('The order in which this committee is listed within a '
                    'project'),
        default=0
    )

    quorum_setting = models.CharField(
        help_text=_('The percentage of committee members required to vote '
                    'in order to have quorum'),
        choices=QUORUM_CHOICES,
        max_length=3
    )
    slug = models.SlugField()
    project = models.ForeignKey('base.Project')
    users = models.ManyToManyField(User)
    objects = models.Manager()

    class Meta:
        """Meta options for the category class."""
        unique_together = (
            ('name', 'project'),
            ('project', 'slug')
        )
        app_label = 'vota'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Committee, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)

    def get_absolute_url(self):
        return reverse('committee-detail', kwargs={
            'project_slug': self.project.slug,
            'slug': self.slug
        })
