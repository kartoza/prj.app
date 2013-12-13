# coding=utf-8
"""
This model is used to create 'committees' of users.

A Committee has many Users
"""

import logging
logger = logging.getLogger(__name__)
from django.db import models
from audited_models.models import AuditedModel
from django.utils.translation import ugettext_lazy as _
from base.models import Project
from django.contrib.auth.models import User


QUORUM_CHOICES = (
    ('All Members', '100'),
    ('Three Quarters', '75'),
    ('Half', '50'),
    ('One Quarter', '25'),
    ('One Member', '1')
)


class Committee(AuditedModel):
    """A category model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text=_('The name of this committee.'),
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    sort_number = models.SmallIntegerField(
        help_text=_('The order in which this committee is listed within a '
                    'project'),
        default=0
    )

    quorum_setting = models.CharField(
        help_text=_('The percentage of committee members required to vote '
                    'in order to have quorum'),
        choices=QUORUM_CHOICES
    )

    project = models.ForeignKey(Project)
    users = models.ManyToManyField(User)
    all_objects = models.Manager()

    class Meta:
        """Meta options for the category class."""
        unique_together = ('name', 'project')
        app_label = 'vota'

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)
