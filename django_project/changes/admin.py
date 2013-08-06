from django.contrib import admin
from models import Project, Category, Version, Entry
from audited_models.admin import AuditedAdmin


class ProjectAdmin(AuditedAdmin):

    def queryset(self, request):
        """Ensure we use the correct manager."""
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class CategoryAdmin(AuditedAdmin):

    def queryset(self, request):
        """Ensure we use the correct manager."""
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class VersionAdmin(AuditedAdmin):

    def queryset(self, request):
        """Ensure we use the correct manager."""
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class EntryAdmin(AuditedAdmin):

    def queryset(self, request):
        """Ensure we use the correct manager."""
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Entry, EntryAdmin)
