# coding=utf-8
"""Training center model definitions for certification apps.

"""

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from .certifying_organisation import (
    CertifyingOrganisation,
    SlugifyingMixin,
    validate_email_address)


class TrainingCenter(SlugifyingMixin, models.Model):
    """Training Centre / Organisation registration."""

    name = models.CharField(
        help_text=_('Training Center name.'),
        max_length=150,
        null=False,
        blank=False,
        unique=True
    )

    email = models.CharField(
        help_text=_('Valid email address for communication purposes.'),
        max_length=150,
        null=False,
        blank=False,
        validators=[validate_email_address]
    )

    address = models.TextField(
        help_text=_(
            'Address of the training center. '
            'If your training center is online, '
            'you can put your web address of your training center.'),
        max_length=250,
        null=False,
        blank=False,
    )

    phone = models.CharField(
        help_text=_('Phone number: (country code)(number) e.g. +6221551553'),
        max_length=150,
        null=False,
        blank=False
    )

    location = models.GeometryField(
        blank=True,
        null=True,
        srid=4326
    )

    slug = models.SlugField()
    certifying_organisation = models.ForeignKey(CertifyingOrganisation,
                                                on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(TrainingCenter, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to training center detail page.

        :return: URL
        :rtype: str
        """
        return reverse('trainingcenter-detail', kwargs={
            'slug': self.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'project_slug': self.certifying_organisation.project.slug
        })
