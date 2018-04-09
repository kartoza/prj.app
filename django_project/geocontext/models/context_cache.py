# coding=utf-8
"""Context Cache Model."""

from django.utils.translation import ugettext_lazy as _

from django.contrib.gis.db import models

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

    geometry = models.GeometryField(
        help_text=_('The 2D geometry of the context.'),
        blank=True,
        null=True,
    )

    geometry_3d = models.GeometryField(
        help_text=_('The 3D geometry of the context.'),
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
