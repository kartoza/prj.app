from django.contrib import admin
from models import Project, Category, Entry


class ProjectAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class EntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
