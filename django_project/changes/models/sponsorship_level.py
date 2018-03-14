# coding=utf-8

import os
from django.conf.global_settings import MEDIA_ROOT
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

__author__ = 'rischan'


class ApprovedSponsorshipLevelManager(models.Manager):
    """Custom sponsor manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            ApprovedSponsorshipLevelManager, self).get_queryset().filter(
                approved=True)


class UnapprovedSponsorshipLevelManager(models.Manager):
    """Custom sponsor manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            UnapprovedSponsorshipLevelManager, self).get_queryset().filter(
                approved=False)


class SponsorshipLevel(models.Model):
    """A sponsor model e.g. gui, backend, web site etc."""

    name = models.CharField(
        help_text='Name of sponsorship level. e.g. Gold, Bronze, etc',
        max_length=255,
        null=False,
        blank=False,
        unique=False)

    value = models.IntegerField(
        help_text='Amount of money associated with this sponsorship level.',
        blank=False,
        null=False,
        unique=False
    )

    currency = models.CharField(
        help_text='The currency which associated with '
                  'this sponsorship level.',
        max_length=255,
        null=False,
        blank=False,
        unique=False)

    logo = models.ImageField(
        help_text=(
            'An image of sponsorship level logo e.g. a bronze medal.'
            'Most browsers support dragging the image directly on to the '
            '"Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=False)

    logo_width = models.IntegerField(
        help_text=(
            'Enter the width of the icon that should be used on the changelog'
        ),
        blank=False,
        null=False,
        default=100
    )

    logo_height = models.IntegerField(
        help_text=(
            'Enter the height of the icon that should be used on the changelog'
        ),
        blank=False,
        null=False,
        default=100
    )

    approved = models.BooleanField(
        help_text=_(
            'Whether this sponsorship level has been approved for use by '
            'the project owner.'),
        default=False
    )

    author = models.ForeignKey(User)
    slug = models.SlugField()
    project = models.ForeignKey('base.Project')
    objects = models.Manager()
    approved_objects = ApprovedSponsorshipLevelManager()
    unapproved_objects = UnapprovedSponsorshipLevelManager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the sponsor class."""
        unique_together = (
            ('name', 'project'),
            ('project', 'slug')
        )
        app_label = 'changes'
        ordering = ['project', '-value']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(SponsorshipLevel, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s : %s %s' % (self.name, self.value, self.currency)

    def get_absolute_url(self):
        return reverse('sponsorshiplevel-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })
