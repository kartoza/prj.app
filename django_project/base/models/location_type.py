# coding=utf-8
"""Location type definition.

"""

from django.db import models
from django.contrib.gis.geos import (
    Point,
    Polygon,
    MultiPolygon,
    LineString,
)


class LocationType(models.Model):
    """Location type model."""

    GEOMETRY_CHOICES = (
        ('POINT', 'Point'),
        ('LINE', 'Line'),
        ('POLYGON', 'Polygon'),
        ('MULTIPOLYGON', 'Multipolygon'),
    )

    ALLOWED_GEOMETRY = {
        'POINT': Point,
        'LINE': LineString,
        'POLYGON': Polygon,
        'MULTIPOLYGON': MultiPolygon,
    }

    name = models.CharField(
        max_length=100,
        blank=False,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    allowed_geometry = models.CharField(
        max_length=20,
        choices=GEOMETRY_CHOICES,
    )

    def get_allowed_geometry_class(self):
        """Return allowed geometry class, e.g. Point"""
        return self.ALLOWED_GEOMETRY[self.allowed_geometry]

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        app_label = 'base'
        ordering = ['name']

    def __str__(self):
        return u'%s' % self.name
