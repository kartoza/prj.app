# coding=utf-8
"""Model admin class definitions."""

from django.contrib import admin

from geocontext.models.context_service_registry import ContextServiceRegistry


class ContextServiceRegistryAdmin(admin.ModelAdmin):
    """Answer admin model."""
    list_display = (
        'name', 'display_name', 'query_type', 'url',
        )

admin.site.register(ContextServiceRegistry, ContextServiceRegistryAdmin)
