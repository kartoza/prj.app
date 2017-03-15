# coding=utf-8
import os
import pytz
import logging
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from unidecode import unidecode


__author__ = 'rischan'

logger = logging.getLogger(__name__)
utc = pytz.UTC


class ApprovedSponsorManager(models.Manager):
    """Custom sponsor manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            ApprovedSponsorManager, self).get_queryset().filter(
                approved=True)


class UnapprovedSponsorManager(models.Manager):
    """Custom sponsor manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            UnapprovedSponsorManager, self).get_queryset().filter(
                approved=False)


# noinspection PyUnresolvedReferences
class Sponsor(models.Model):
    """A sponsor model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text=_('Name of sponsor.'),
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    sponsor_url = models.CharField(
        help_text='Input the sponsor URL.',
        max_length=255,
        null=True,
        blank=True)

    contact_person = models.CharField(
        help_text='Input the contact person of sponsor.',
        max_length=255,
        null=True,
        blank=True)

    address = models.TextField(
        help_text=(
            'Enter the complete street address for this sponsor. '
            'Use line breaks to separate address elements and use '
            'the country field to specify the country.'
        ),
        null=True,
        blank=True)

    country = CountryField(
        help_text='Select the country for this sponsor',
        null=True,
        blank=True)

    sponsor_email = models.CharField(
        help_text='Input an email of sponsor.',
        max_length=255,
        null=True,
        blank=True)

    agreement = models.FileField(
        help_text='Attach sponsor agreement',
        upload_to=os.path.join(MEDIA_ROOT, 'docs'),
        blank=True)

    logo = models.ImageField(
        help_text=(
            'An image of sponsor logo e.g. a splashscreen. '
            'Most browsers support dragging the image directly on to the '
            '"Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=False)

    approved = models.BooleanField(
        help_text=_(
            'Whether this sponsor has been approved for use by the '
            'project owner.'),
        default=False
    )

    author = models.ForeignKey(User)
    slug = models.SlugField()
    project = models.ForeignKey('base.Project')
    objects = models.Manager()
    approved_objects = ApprovedSponsorManager()
    unapproved_objects = UnapprovedSponsorManager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the sponsor class."""
        unique_together = (
            ('name', 'project'),
            ('project', 'slug')
        )
        app_label = 'changes'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(Sponsor, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.name)

    def get_absolute_url(self):
        return reverse('sponsor-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })
