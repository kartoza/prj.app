# coding=utf-8
"""
Certifying organisation model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class SlugifyingMixin(object):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(SlugifyingMixin, self).save(*args, **kwargs)


class ApprovedCertifyingOrganisationManager(models.Manager):
    def get_queryset(self):
        return super(
            ApprovedCertifyingOrganisationManager, self).get_queryset().filter(
                approved=True)


class UnapprovedCertifyingOrganisationManager(models.Manager):
    def get_queryset(self):
        return super(
            UnapprovedCertifyingOrganisationManager, self).get_queryset(
        ).filter(approved=False)


class CertifyingOrganisation(SlugifyingMixin, models.Model):
    """ Certifying organisation model."""

    name = models.CharField(
        help_text="Name of Organisation or Institution.",
        max_length=200,
        null=False,
        blank=False
    )

    organisation_email = models.CharField(
        help_text="Email address Organisation or Institution.",
        max_length=200,
        null=False,
        blank=False
    )

    address = models.CharField(
        help_text="Contact of Organisation or Institution.",
        max_length=200,
        null=False,
        blank=False
    )

    organisation_phone = models.CharField(
        help_text="Contact of Organisation or Institution.",
        max_length=200,
        null=False,
        blank=False
    )

    approved = models.BooleanField(
        help_text="Approval from project admin",
        default=False
    )

    slug = models.SlugField()
    author = models.ForeignKey(User)
    project = models.ForeignKey('base.Project')
    objects = models.Manager()
    approved_objects = ApprovedCertifyingOrganisationManager()
    unapproved_objects = UnapprovedCertifyingOrganisationManager()

    # noinspection PyClassicStyleClass.
    class Meta:
        """ Meta class for Course attendee."""
        app_label = 'certification'
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(CertifyingOrganisation, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to certifying organisation detail page.
        :return: URL
        :rtype: str
        """
        return reverse('certifying-organisation-detail', kwargs={
                'slug': self.slug,
                'project_slug': self.project.slug
        })
