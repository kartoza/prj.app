"""
This model is to create "ballots" i.e. questions/proposals/changes which a
Committee can vote on.

After voting is complete, a ballot should be marked as either Denied or Passed.

If no quorum is reached, no_quorum should be True

A ballot has one Committee.
"""
import logging

logger = logging.getLogger(__name__)
from django.db import models
from audited_models.models import AuditedModel
from django.utils.translation import ugettext_lazy as _


class PassedCategoryManager(models.Manager):
    """Custom category manager that shows only passed ballots."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            PassedCategoryManager, self).get_query_set().filter(
                passed=True)


class DeniedCategoryManager(models.Manager):
    """Custom version manager that shows only denied ballots."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            DeniedCategoryManager, self).get_query_set().filter(
                denied=True)


class Ballot(AuditedModel):
    """A category model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text=_('Name of this ballot.'),
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    description = models.CharField(
        help_text=_('The content of this ballot; the details on which the '
                    'Committee should base their vote.'),
        max_length=3000,
        null=False,
        blank=False,
    )

    approved = models.BooleanField(
        help_text=_(
            'Whether this ballot has been approved.'),
        default=False
    )

    denied = models.BooleanField(
        help_text=_(
            'Whether this ballot has been denied.'),
        default=False
    )

    no_quorum = models.BooleanField(
        help_text=_('Whether the ballot was denied because no quorum was '
                    'reached'),
        default=False
    )

    # noinspection PyUnresolvedReferences
    committee = models.ForeignKey('Committee')

    all_objects = models.Manager()
    passed_objects = PassedCategoryManager()
    denied_objects = DeniedCategoryManager()

    class Meta:
        """Meta options for the category class."""
        unique_together = ('name', 'committee')
        app_label = 'vota'

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)
