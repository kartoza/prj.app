# coding=utf-8
"""Context Cache Model."""

from django.utils.translation import ugettext_lazy as _

from django.contrib.gis.db import models

from geocontext.utilities import convert_2d_to_3d
from geocontext.models.context_service_registry import ContextServiceRegistry



class ContextCache(models.Model):
    """Context Cache Model Class."""

    name = models.CharField(
        help_text=_('Name of Cache Context.'),
        blank=False,
        null=False,
        max_length=200,
    )

    source_uri = models.CharField(
        help_text=_('Source URI of the Context.'),
        blank=False,
        null=False,
        max_length=1000,
    )

    geometry_linestring = models.LineStringField(
        help_text=_('The line geometry of the context.'),
        blank=True,
        null=True,
        dim=3
    )

    geometry_multi_linestring = models.MultiLineStringField(
        help_text=_('The multi line geometry of the context.'),
        blank=True,
        null=True,
        dim=3
    )

    geometry_polygon = models.PolygonField(
        help_text=_('The polygon geometry of the context.'),
        blank=True,
        null=True,
        dim=3
    )

    geometry_multi_polygon = models.MultiPolygonField(
        help_text=_('The multi polygon geometry of the context.'),
        blank=True,
        null=True,
        dim=3
    )

    service_registry = models.ForeignKey(
        ContextServiceRegistry,
        help_text=_('Service registry where the context comes from'),
        on_delete=models.CASCADE
    )

    value = models.CharField(
        help_text=_('The value of the context.'),
        blank=False,
        null=False,
        max_length=200,
    )

    expired_time = models.DateTimeField(
        help_text=_('When the cache expired.'),
        blank=False,
        null=False
    )

    def set_geometry_field(self, geometry):
        """Set geometry field based on the type

        :param geometry: The geometry.
        :type geometry: GEOSGeometry
        """
        if not geometry.hasz:
            geometry = convert_2d_to_3d(geometry)

        if geometry.geom_type in ['LineString', 'LinearRing']:
            self.geometry_linestring = geometry
        elif geometry.geom_type == 'Polygon':
            self.geometry_polygon = geometry
        elif geometry.geom_type == 'MultiLineString':
            self.geometry_multi_linestring = geometry
        elif geometry.geom_type == 'MultiPolygon':
            self.geometry_multi_polygon = geometry

    @property
    def geometry(self):
        """Attribute for geometry

        :return: The geometry of the cache
        :rtype: GEOSGeometry
        """
        if self.geometry_linestring:
            return self.geometry_linestring
        elif self.geometry_polygon:
            return self.geometry_polygon
        elif self.geometry_multi_linestring:
            return self.geometry_linestring
        elif self.geometry_multi_polygon:
            return self.geometry_multi_polygon
        else:
            return None
