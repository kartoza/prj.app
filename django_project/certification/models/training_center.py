# coding=utf-8
"""
Training center model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from certifying_organisation import CertifyingOrganisation, SlugifyingMixin
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class TrainingCenter(SlugifyingMixin, models.Model):
    """Training Centre / Organisation registration."""

    name = models.CharField(
        help_text=_('Organisation/Institution name.'),
        max_length=150,
        null=False,
        blank=False,
        unique=True
    )

    email = models.CharField(
        help_text=_('Valid email address for communication purpose.'),
        max_length=150,
        null=False,
        blank=False
    )

    address = models.TextField(
        help_text=_('Address of the organisation/institution.'),
        max_length=250,
        null=False,
        blank=False,
    )

    phone = models.CharField(
        help_text=_('Phone number/Landline.'),
        max_length=150,
        null=False,
        blank=False
    )

    location = models.PointField(blank=True, null=True,
                                 default='POINT(28.034088 -26.195246)')

    slug = models.SlugField()
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    author = models.ForeignKey(User)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(TrainingCenter, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to training center detail page.
        :return: URL
        :rtype: str
        """
        return reverse('training-center-detail', kwargs={
            'slug': self.slug,
        })
