"""
This model is to create "ballots" i.e. questions/proposals/changes which a
Committee can vote on.

After voting is complete, a ballot should be marked as either Denied or Passed.

If no quorum is reached, no_quorum should be True

A ballot has one Committee.
"""
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import logging
from core.settings.contrib import STOP_WORDS

logger = logging.getLogger(__name__)
from django.db import models
from audited_models.models import AuditedModel
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from vota.models.vote import Vote
import datetime
from django.contrib.auth.models import User


class ApprovedCategoryManager(models.Manager):
    """Custom category manager that shows only approved ballots."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedCategoryManager, self).get_query_set().filter(
                approved=True)


class DeniedCategoryManager(models.Manager):
    """Custom version manager that shows only denied ballots."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            DeniedCategoryManager, self).get_query_set().filter(
                denied=True)


class OpenBallotManager(models.Manager):
    """Custom version manager that shows only open ballots."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            OpenBallotManager, self).get_query_set().filter(
                open_from__lt=timezone.now())


class ClosedBallotManager(models.Manager):
    """Custom version manager that shows only closed ballots."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ClosedBallotManager, self).get_query_set().filter(
                closes__gt=timezone.now())


class Ballot(AuditedModel):
    """A category model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text=_('Name of this ballot.'),
        max_length=255,
        null=False,
        blank=False,
        unique=False
    )  # there is a unique together rule in meta class below

    summary = models.CharField(
        help_text=_('A brief overview of the ballot.'),
        max_length=250,
        blank=False,
        null=False
    )

    description = models.TextField(
        help_text=_('A full description of the proposal if a summary is not '
                    'enough!'),
        max_length=3000,
        null=True,
        blank=True,
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

    open_from = models.DateTimeField(
        help_text=_('Date the ballot opens'),
        default=timezone.now()
    )

    closes = models.DateTimeField(
        help_text=_('Date the ballot closes'),
        default=timezone.now() + datetime.timedelta(days=7)
    )

    private = models.BooleanField(
        help_text=_('Should members be prevented from viewing results before '
                    'voting?'),
        default=False
    )

    proposer = models.ForeignKey(User)
    # noinspection PyUnresolvedReferences
    committee = models.ForeignKey('Committee')
    slug = models.SlugField()
    objects = models.Manager()
    approved_objects = ApprovedCategoryManager()
    denied_objects = DeniedCategoryManager()
    open_objects = OpenBallotManager()
    closed_objects = ClosedBallotManager()

    class Meta:
        """Meta options for the category class."""
        unique_together = (
            ('name', 'committee'),
            ('committee', 'slug')
        )
        app_label = 'vota'

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(Ballot, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s : %s' % (self.committee.name, self.name)

    def get_absolute_url(self):
        return reverse('ballot-detail', kwargs={
            'project_slug': self.committee.project.slug,
            'committee_slug': self.committee.slug,
            'slug': self.slug
        })

    def get_user_voted(self, user=None):
        voted = False
        if Vote.objects.filter(ballot=self).filter(user=user).exists():
            voted = True
        return voted

    def get_positive_vote_count(self):
        votes = Vote.objects.filter(ballot=self).filter(positive=True).count()
        return votes

    def get_negative_vote_count(self):
        votes = Vote.objects.filter(ballot=self).filter(negative=True).count()
        return votes

    def get_abstainer_count(self):
        votes = Vote.objects.filter(ballot=self).filter(abstain=True).count()
        return votes

    def get_current_tally(self):
        positive = self.get_positive_vote_count()
        negative = self.get_negative_vote_count()
        tally = 0
        tally += positive
        tally -= negative
        return tally

    def get_total_vote_count(self):
        vote_count = Vote.objects.filter(ballot=self).count()
        return vote_count

    def has_quorum(self):
        vote_count = self.get_total_vote_count()
        committee_user_count = self.committee.users.all().count()
        if committee_user_count != 0:
            quorum_percent = self.committee.quorum_setting
            percentage = 100 * float(vote_count) / float(committee_user_count)
            if percentage > quorum_percent:
                return True
        else:
            return False
