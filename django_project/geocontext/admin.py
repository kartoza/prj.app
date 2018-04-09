# coding=utf-8
"""Model admin class definitions."""

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from geocontext.models.context_service_registry import ContextServiceRegistry
from geocontext.models.context_cache import ContextCache


class ContextServiceRegistryAdmin(admin.ModelAdmin):
    """Context Service Registry admin model."""
    list_display = ('name', 'display_name', 'query_type', 'url')


class ContextCacheAdmin(OSMGeoAdmin):
    """Context Cache admin model."""
    list_display = ('name', 'service_registry', 'value', 'expired_time')


admin.site.register(ContextServiceRegistry, ContextServiceRegistryAdmin)
admin.site.register(ContextCache, ContextCacheAdmin)
