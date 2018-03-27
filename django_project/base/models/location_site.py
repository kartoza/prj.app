# coding=utf-8
"""Site model definition.

"""

from django.core.exceptions import ValidationError
from django.contrib.gis.db import models
from base.models.location_type import LocationType


class LocationSite(models.Model):
    """Location Site model."""

    name = models.CharField(
        max_length=100,
        blank=False,
    )
    location_type = models.ForeignKey(
        LocationType,
        models.CASCADE,
        null=False,
    )
    geometry_point = models.PointField(
        null=True,
        blank=True,
    )
    geometry_line = models.LineStringField(
        null=True,
        blank=True,
    )
    geometry_polygon = models.PolygonField(
        null=True,
        blank=True,
    )
    geometry_multipolygon = models.MultiPolygonField(
        null=True,
        blank=True,
    )

    def get_geometry(self):
        """Function to get geometry."""
        geometry = None
        validation_error = ValidationError('Only one geometry allowed.')

        if self.geometry_point:
            if geometry:
                raise validation_error
            geometry = self.geometry_point

        if self.geometry_polygon:
            if geometry:
                raise validation_error
            geometry = self.geometry_polygon

        if self.geometry_multipolygon:
            if geometry:
                raise validation_error
            geometry = self.geometry_multipolygon

        if self.geometry_line:
            if geometry:
                raise validation_error
            geometry = self.geometry_line

        return geometry

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        app_label = 'base'

    def __str__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        """Check if one of geometry is not null."""
        if self.geometry_point or self.geometry_line or \
                self.geometry_polygon or self.geometry_multipolygon:
            # Check if geometry is allowed
            if isinstance(self.get_geometry(),
                          self.location_type.get_allowed_geometry_class()):
                super(LocationSite, self).save(*args, **kwargs)
            else:
                raise ValidationError('Geometry is not allowed.')
        else:
            raise ValidationError('At least one geometry need to be filled.')
