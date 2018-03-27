# coding=utf-8
"""IUCN Status model definition.

"""

from django.db import models


class IUCNStatus(models.Model):
    """IUCN status model."""

    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )
    narrative = models.TextField(
        blank=True,
    )
    sensitive = models.BooleanField(
        default=False
    )

    def __str__(self):
        return u'%s' % self.name

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        app_label = 'fish'
        verbose_name_plural = 'IUCN Status'
        verbose_name = 'IUCN Status'
