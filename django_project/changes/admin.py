from django.contrib import admin
from models import Project, Category, Version, Entry
from audited_models.admin import AuditedAdmin


class ProjectAdmin(AuditedAdmin):
    pass


class CategoryAdmin(AuditedAdmin):
    pass


class VersionAdmin(AuditedAdmin):
    pass


class EntryAdmin(AuditedAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Entry, EntryAdmin)
