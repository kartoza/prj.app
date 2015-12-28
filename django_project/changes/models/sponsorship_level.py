# coding=utf-8

import os
from django.conf.global_settings import MEDIA_ROOT
from django.db import models

__author__ = 'rischan'

WORLD_CURRENCY = (
    (1, 'Euro'),
    (2, 'US Dollar'),
    (3, 'ZAR')
)


class ApprovedSponsorshipLevelManager(models.Manager):
    """Custom sponsor manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            ApprovedSponsorshipLevelManager, self).get_queryset().filter(
                approved=True)


class UnapprovedSponsorshipLevelManager(models.Manager):
    """Custom sponsor manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            UnapprovedSponsorshipLevelManager, self).get_queryset().filter(
                approved=False)


class SponsorshipLevel(models.Model):
    """A sponsor model e.g. gui, backend, web site etc."""
    project = models.ForeignKey(to='base.Project')

    value = models.IntegerField(
        help_text='Amount of money associated with this sponsorship level.',
        blank=False,
        null=False,
        unique=False
    )

    currency = models.IntegerField(
        help_text='The currency which associated with this sponsorship level.',
        choices=WORLD_CURRENCY)

    name = models.CharField(
        help_text='Name of sponsorship level. e.g. Gold, Bronze, etc',
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    logo = models.ImageField(
        help_text=(
            'An image of sponsorship level logo e.g. a bronze medal.'
            'Most browsers support dragging the image directly on to the '
            '"Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=False)

    def __unicode__(self):
        return '%s' % (self.name)

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the sponsorship level class."""
        unique_together = (
            ('name', 'project'),
            ('project', 'value')
        )
        app_label = 'changes'
        ordering = ['project', 'value']
