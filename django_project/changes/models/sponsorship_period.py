__author__ = 'rischan'

import datetime
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SponsorshipPeriod(models.Model):
    """A sponsorship period model e.g. gui, backend, web site etc."""
    sponsor = models.ForeignKey('Sponsor')

    start_date = models.DateField(
        _("Start date"),
        default=timezone.now)

    end_date = models.DateField(
        _("End date"),
        default=timezone.now)

    sponsorshiplevel = models.ForeignKey('SponsorshipLevel')

    def __unicode__(self):
        return '%s' % self.sponsor

    def current_sponsor(self):
        today = timezone.now()
        start = self.start_date
        end = self.end_date
        if start < today < end:
            return True
        else:
            return False
