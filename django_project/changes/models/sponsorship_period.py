__author__ = 'rischan'

import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SponsorshipPeriod(models.Model):
    """A sponsorship period model e.g. gui, backend, web site etc."""
    sponsor = models.ForeignKey('Sponsor')

    start_date = models.DateField(
        _("Start date"),
        default=datetime.date.today())

    end_date = models.DateField(
        _("End date"),
        default=datetime.date.today())

    def __unicode__(self):
        return '%s' % self.sponsor
