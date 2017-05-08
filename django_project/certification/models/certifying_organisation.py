# coding=utf-8
"""Certifying organisation model definitions for certification apps.

"""

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from django.contrib.auth.models import User
from django_countries.fields import CountryField
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
    """Custom training centre manager.

    Shows only approved certifying organisation.
    """

    def get_queryset(self):
        """Query set generator. """

        return super(
            ApprovedCertifyingOrganisationManager, self).get_queryset().filter(
                approved=True)


class UnapprovedCertifyingOrganisationManager(models.Manager):
    """Custom training centre manager.

    Shows only unapproved certifying organisation.
    """

    def get_queryset(self):
        """Query set generator. """

        return super(
            UnapprovedCertifyingOrganisationManager, self).get_queryset(
        ).filter(approved=False)


def validate_email_address(value):
    try:
        validate_email(value)
        return True
    except ValidationError(
            _('%(value)s is not a valid email address'),
            params={'value': value},):
        return False


class CertifyingOrganisation(SlugifyingMixin, models.Model):
    """Certifying organisation model."""

    name = models.CharField(
        help_text='Name of Organisation or Institution.',
        max_length=200,
        null=False,
        blank=False,
        unique=True
    )

    organisation_email = models.CharField(
        help_text='Email address Organisation or Institution.',
        max_length=200,
        null=False,
        blank=False,
        validators=[validate_email_address],
    )

    address = models.TextField(
        help_text='Address of Organisation or Institution.',
        max_length=1000,
        null=False,
        blank=False
    )

    country = CountryField(
        help_text='Select the country for this Institution',
        null=True,
        blank=True)

    organisation_phone = models.CharField(
        help_text='Phone number: (country code)(number) e.g. +6221551553',
        max_length=200,
        null=False,
        blank=False
    )

    approved = models.BooleanField(
        help_text='Approval from project admin',
        default=False
    )

    enabled = models.BooleanField(
        help_text='Project enabled',
        default=True
    )

    slug = models.SlugField()
    organisation_owners = models.ManyToManyField(User)
    project = models.ForeignKey('base.Project')
    objects = models.Manager()
    approved_objects = ApprovedCertifyingOrganisationManager()
    unapproved_objects = UnapprovedCertifyingOrganisationManager()

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Course attendee."""

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
