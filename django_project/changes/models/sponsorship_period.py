# coding=utf-8

import string
import random
import datetime
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
# noinspection PyPackageRequirements
from core.settings.contrib import STOP_WORDS
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from easy_thumbnails.files import get_thumbnailer

__author__ = 'rischan'


class ApprovedSponsorshipPeriodManager(models.Manager):
    """Custom sponsor manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            ApprovedSponsorshipPeriodManager, self).get_queryset().filter(
                approved=True)


class UnapprovedSponsorshipPeriodManager(models.Manager):
    """Custom sponsor manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            UnapprovedSponsorshipPeriodManager, self).get_queryset().filter(
                approved=False)


class SponsorshipPeriod(models.Model):
    """A sponsorship period model e.g. gui, backend, web site etc."""

    start_date = models.DateField(
        _("Start date"),
        help_text='Start date of sustaining membership period',
        default=timezone.now)

    end_date = models.DateField(
        _("End date"),
        help_text='End date of sustaining membership period',
        null=True,
        blank=True
    )

    amount_sponsored = models.DecimalField(
        _('Amount Sponsored'),
        help_text=_('The actual amount sponsored for this period.'),
        decimal_places=2,
        max_digits=30,
        null=True,
        blank=True,
    )

    currency = models.CharField(
        help_text=_('The currency that is used for '
                    'sustaining membership payment.'),
        max_length=50,
        null=True,
        blank=True,
        default='EUR'
    )

    approved = models.BooleanField(
        help_text=_(
            'Whether this sponsorship period has been approved for use by '
            'the project owner.'),
        default=False
    )

    recurring = models.BooleanField(
        help_text=_(
            'Bill customer at the start of each period'
        ),
        default=False
    )

    subscription = models.ForeignKey(
        'djstripe.Subscription',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    project = models.ForeignKey('base.Project', on_delete=models.CASCADE)
    objects = models.Manager()
    approved_objects = ApprovedSponsorshipPeriodManager()
    unapproved_objects = UnapprovedSponsorshipPeriodManager()
    # noinspection PyUnresolvedReferences
    sponsor = models.ForeignKey(
        'Sponsor',
        verbose_name='Sustaining member',
        on_delete=models.CASCADE,
        help_text='Input the sustaining member name',
    )
    # noinspection PyUnresolvedReferences
    sponsorship_level = models.ForeignKey(
        'SponsorshipLevel',
        verbose_name='Sustaining member level',
        on_delete=models.CASCADE,
        help_text='This level take from Sustaining Membership Level, '
        'you can add it by using Sustaining Membership Level menu',
    )
    # noinspection PyClassicStyleClass

    class Meta:
        """Meta options for the sponsor class."""
        unique_together = (
            ('project', 'slug')
        )
        app_label = 'changes'
        ordering = ['project', '-end_date']
        verbose_name = 'Sustaining Member Period'
        verbose_name_plural = 'Sustaining Member Periods'

    def save(self, *args, **kwargs):
        if not self.pk:
            name = self.slug_generator()
            words = name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(SponsorshipPeriod, self).save(*args, **kwargs)

    @staticmethod
    def slug_generator(size=6, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def __unicode__(self):
        plan = None
        if self.sponsorship_level.subscription_plan and self.recurring:
            plan = self.sponsorship_level.subscription_plan.interval
            plan = '{}ly'.format(plan.capitalize())
        return u'%s - %s : %s' % (
            self.sponsor.name,
            self.start_date,
            plan if plan else self.end_date
        )

    def get_absolute_url(self):
        return reverse('sponsorshipperiod-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })

    def current_sponsor(self):
        today = datetime.datetime.now().date()
        end = self.end_date
        start = self.start_date
        if end < today or start > today:
            return False
        else:
            return True

    def future_sponsor(self):
        today = datetime.datetime.now().date()
        end = self.end_date
        start = self.start_date
        if end < today or start < today:
            return False
        else:
            return True

    def logo_url(self):
        """Get the logo url sampled according to the size of sponsorship.

        The idea here is that large sponsors get large logos and small
        sponsors get small ones. You can specify the width and height in the
        logo_height and logo_width properties.

        This method is intended mainly for use from within your html templates.

        :returns: A url to the resampled logo
        :rtype: str
        """
        options = {'size': (
            self.sponsorship_level.logo_width,
            self.sponsorship_level.logo_height), 'crop': False}
        thumb_url = ''
        thumb_url = get_thumbnailer(
                self.sponsor.logo).get_thumbnail(options).url
        return thumb_url
