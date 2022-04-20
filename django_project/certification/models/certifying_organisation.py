# coding=utf-8
"""Certifying organisation model definitions for certification apps.

"""

import os
from django.conf.global_settings import MEDIA_ROOT
from django.urls import reverse
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
from simple_history.models import HistoricalRecords
from certification.utilities import check_slug
from certification.models.status import Status

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
        ).filter(approved=False, rejected=False)


def validate_email_address(value):
    try:
        validate_email(value)
        return True
    except ValidationError:
        raise ValidationError(
            _('%(value)s is not a valid email address'),
            params={'value': value},
        )


class CertifyingOrganisation(models.Model):
    """Certifying organisation model."""

    name = models.CharField(
        help_text=_('Name of organisation or institution'),
        max_length=200,
        null=False,
        blank=False
    )

    organisation_email = models.CharField(
        help_text=_('Email address organisation or institution.'),
        max_length=200,
        null=False,
        blank=False,
        validators=[validate_email_address],
    )

    url = models.URLField(
        help_text=u'Optional URL for the certifying organisation\'s home page',
        blank=True,
        null=True
    )

    address = models.TextField(
        help_text=_('Address of Organisation or Institution.'),
        max_length=1000,
        null=False,
        blank=False
    )

    logo = models.ImageField(
        help_text=_('Logo for this organisation. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/organisations'),
        blank=True
    )

    country = CountryField(
        help_text=_('Select the country for this Institution'),
        null=True,
        blank=True)

    organisation_phone = models.CharField(
        help_text=_('Phone number: (country code)(number) e.g. +6221551553'),
        max_length=200,
        null=False,
        blank=False
    )

    organisation_credits = models.IntegerField(
        help_text=_('Credits available'),
        default=0,
        null=True,
        blank=True
    )

    approved = models.BooleanField(
        help_text=_('Approval from project admin'),
        default=False
    )

    enabled = models.BooleanField(
        help_text=_('Project enabled'),
        default=True
    )

    rejected = models.BooleanField(
        help_text=_('Rejection from project admin'),
        default=False
    )

    status = models.ForeignKey(
        Status,
        null=True,
        blank=True, on_delete=models.SET_NULL
    )

    remarks = models.CharField(
        help_text=_(
            'Remarks regarding status of this organisation, '
            'i.e. Rejected, because lacks of information'),
        max_length=500,
        null=True,
        blank=True
    )

    owner_message = models.TextField(
        help_text=_(
            'Message from owner of this organisation.'
        ),
        null=True,
        blank=True
    )

    history = HistoricalRecords()

    slug = models.SlugField()
    organisation_owners = models.ManyToManyField(User)
    project = models.ForeignKey('base.Project', on_delete=models.CASCADE)
    objects = models.Manager()
    approved_objects = ApprovedCertifyingOrganisationManager()
    unapproved_objects = UnapprovedCertifyingOrganisationManager()

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Course attendee."""

        app_label = 'certification'
        ordering = ['name']
        unique_together = ['name', 'project']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            new_slug = slugify(new_list)[:50]
            new_slug = \
                check_slug(CertifyingOrganisation.objects.all(), new_slug)
            self.slug = slugify(new_slug)[:50]
        super(CertifyingOrganisation, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s - %s' % (self.project.name, self.name)

    def __str__(self):
        return '%s - %s' % (self.project.name, self.name)

    @property
    def creation_date(self):
        return self.history.earliest().history_date

    @property
    def update_date(self):
        return self.history.latest().history_date

    def get_absolute_url(self):
        """Return URL to certifying organisation detail page.

        :return: URL
        :rtype: str
        """
        return reverse('certifyingorganisation-detail', kwargs={
                'slug': self.slug,
                'project_slug': self.project.slug
        })
