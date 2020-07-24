# coding=utf-8
"""Model admin class definitions.

Note these admin models inherit reversion (which provides
historization for a model).

..note:: if you add reversion.VersionAdmin to a model be sure to do
    ``./manage.py createinitialrevisions``.

.. see also:: https://github.com/etianen/django-reversion/wiki#getting
    -started-with-django-reversion

"""


from django.contrib import admin
from .models import (Category, Version,
                     Entry, Sponsor, SponsorshipLevel,
                     SponsorshipPeriod)
import reversion


class CategoryAdmin(reversion.admin.VersionAdmin):
    """Category admin model."""

    list_filter = ('project',)
    search_fields = ('name',)

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class VersionAdmin(reversion.admin.VersionAdmin):
    """Version admin model."""

    list_display = ('__unicode__', 'project',)

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class EntryAdmin(reversion.admin.VersionAdmin):
    """Entry admin model."""

    list_display = ['pk', 'version_name', 'category', 'title']
    list_filter = ['category']

    def version_name(self, obj):
        return obj.version.name

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class SponsorAdmin(reversion.admin.VersionAdmin):
    """Sponsor admin model."""

    list_display = ['__unicode__', 'project']
    search_fields = ['name']

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class SponsorLevelAdmin(reversion.admin.VersionAdmin):
    """Sponsor level admin model."""

    list_display = ['__unicode__', 'project']

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class SponsorRenewedAdmin(reversion.admin.VersionAdmin):
    """Renewed sponsor admin model."""

    list_display = ['__unicode__', 'project']

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(Category, CategoryAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SponsorshipLevel, SponsorLevelAdmin)
admin.site.register(SponsorshipPeriod, SponsorRenewedAdmin)
