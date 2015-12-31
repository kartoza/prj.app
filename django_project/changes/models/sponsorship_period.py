__author__ = 'rischan'

import string
import random
from datetime import date
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


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

    start_date = models.DateField(
        _("Start date"),
        help_text='Start date of sponsorship period',
        default=timezone.now)

    end_date = models.DateField(
        _("End date"),
        help_text='End date of sponsorship period',
        default=timezone.now)

    approved = models.BooleanField(
        help_text=_(
            'Whether this sponsorship period has been approved for use by '
            'the project owner.'),
        default=False
    )

    author = models.ForeignKey(User)
    slug = models.SlugField()
    project = models.ForeignKey('base.Project')
    objects = models.Manager()
    approved_objects = ApprovedSponsorshipPeriodManager()
    unapproved_objects = UnapprovedSponsorshipPeriodManager()
    sponsor = models.ForeignKey(
            'Sponsor',
            help_text='Input the sponsor name',
    )
    sponsorshiplevel = models.ForeignKey(
            'SponsorshipLevel',
            help_text='This level take from Sponsorship Level, '
            'you can add it by using Sponsorship Level menu',
    )
    # noinspection PyClassicStyleClass

    class Meta:
        """Meta options for the sponsor class."""
        unique_together = (
            ('project', 'slug')
        )
        app_label = 'changes'
        ordering = ['start_date']

    def save(self, *args, **kwargs):

        if not self.pk:
            name = self.slug_generator()
            words = name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(SponsorshipPeriod, self).save(*args, **kwargs)

    def slug_generator(self, size=6, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def __unicode__(self):
        return u'%s - %s : %s' % (
            self.start_date,
            self.end_date
        )

    def get_absolute_url(self):
        return reverse('sponsorshipperiod-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })

    def current_sponsor(self):
        today = date.today()
        end = self.end_date
        if end < today:
            return False
        else:
            return True
