# coding=utf-8
"""Taxon model definition.

"""

from django.db import models
from fish.models.iucn_status import IUCNStatus


class Taxon(models.Model):
    """Taxon model."""

    gbif_id = models.IntegerField(
        verbose_name='GBIF id',
        null=True,
        blank=True,
    )
    iucn_status = models.ForeignKey(
        IUCNStatus,
        models.SET_NULL,
        null=True,
    )
    common_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )
    scientific_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )
    author = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        app_label = 'fish'
        verbose_name_plural = 'Taxa'
        verbose_name = 'Taxon'

    def __str__(self):
        return "%s (%s)" % (self.common_name, self.iucn_status)
