__author__ = 'rischan'

import datetime
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ApprovedSponsorshipPeriodManager(models.Manager):
    """Custom sponsor manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            ApprovedSponsorshipPeriodManager, self).get_queryset().filter(
                approved=True)


class UnapprovedSponsorshipPeriodManager(models.Manager):
    """Custom sponsor manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            UnapprovedSponsorshipPeriodManager, self).get_queryset().filter(
                approved=False)


class SponsorshipPeriod(models.Model):
    """A sponsorship period model e.g. gui, backend, web site etc."""
    project = models.ForeignKey('base.Project')

    start_date = models.DateField(
        _("Start date"),
        help_text='Start date of sponsorship period',
        default=timezone.now)

    end_date = models.DateField(
        _("End date"),
        help_text='End date of sponsorship period',
        default=timezone.now)

    sponsorshiplevel = models.ForeignKey(
            'SponsorshipLevel',
            help_text='This level take from Sponsorship Level, '
                      'you can add it by using Sponsorship Level menu',
    )

    def __unicode__(self):
        return '%s' % self.project

    def current_sponsor(self):
        today = timezone.now()
        start = self.start_date
        end = self.end_date
        if start < today < end:
            return True
        else:
            return False
