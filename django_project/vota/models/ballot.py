"""
This model is to create "ballots" i.e. questions/proposals/changes which a
Committee can vote on.

After voting is complete, a ballot should be marked as either Denied or Passed.

If no quorum is reached, no_quorum should be True

A ballot has one Committee.
"""
from django.urls import reverse
from django.utils.text import slugify
import logging
from core.settings.contrib import STOP_WORDS

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from vota.models.vote import Vote
import datetime
from django.contrib.auth.models import User
from certification.utilities import check_slug

logger = logging.getLogger(__name__)


class ApprovedCategoryManager(models.Manager):
    """Custom category manager that shows only approved ballots."""

    def get_query_set(self):
        """Query set generator."""
        return super(
            ApprovedCategoryManager, self).get_query_set().filter(
                approved=True)


class DeniedCategoryManager(models.Manager):
    """Custom version manager that shows only denied ballots."""

    def get_query_set(self):
        """Query set generator."""
        return super(
            DeniedCategoryManager, self).get_query_set().filter(
                denied=True)


class OpenBallotManager(models.Manager):
    """Custom version manager that shows only open ballots."""

    def get_query_set(self):
        """Query set generator."""
        return super(
            OpenBallotManager, self).get_query_set().filter(
            closes__gt=timezone.now)


class ClosedBallotManager(models.Manager):
    """Custom version manager that shows only closed ballots."""

    def get_query_set(self):
        """Query set generator."""
        return super(
            ClosedBallotManager, self).get_query_set().filter(
                closes__gt=timezone.now())


def closes_default_time():
    return timezone.now() + datetime.timedelta(days=7)


class Ballot(models.Model):
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
        default=timezone.now
    )

    closes = models.DateTimeField(
        help_text=_('Date the ballot closes'),
        default=closes_default_time
    )

    private = models.BooleanField(
        help_text=_('Should members be prevented from viewing results before '
                    'voting?'),
        default=False
    )

    proposer = models.ForeignKey(User, on_delete=models.CASCADE)
    # noinspection PyUnresolvedReferences
    committee = models.ForeignKey('Committee', on_delete=models.CASCADE)
    slug = models.SlugField()
    objects = models.Manager()
    approved_objects = ApprovedCategoryManager()
    denied_objects = DeniedCategoryManager()
    open_objects = OpenBallotManager()
    closed_objects = ClosedBallotManager()

    # noinspection PyClassicStyleClass
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
            new_slug = slugify(new_list)[:50]
            new_slug = check_slug(Ballot.objects.all(), new_slug)
            self.slug = slugify(new_slug)[:50]
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
        votes = (
            Vote.objects.filter(
                ballot=self, user__in=self.committee.users.all()
            ).filter(choice='y').count())
        return votes

    def get_negative_vote_count(self):
        votes = (
            Vote.objects.filter(
                ballot=self, user__in=self.committee.users.all()
            ).filter(choice='n').count())
        return votes

    def get_abstainer_count(self):
        votes = (
            Vote.objects.filter(
                ballot=self, user__in=self.committee.users.all()
            ).filter(choice='-').count())
        return votes

    def get_current_tally(self):
        positive = self.get_positive_vote_count()
        negative = self.get_negative_vote_count()
        tally = 0
        tally += positive
        tally -= negative
        return tally

    def get_total_vote_count(self):
        vote_count = (
            Vote.objects.filter(
                ballot=self, user__in=self.committee.users.all()).count())
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

    def is_open(self):
        open_date = self.open_from
        close_date = self.closes
        if open_date < timezone.now() < close_date:
            return True
        return False
