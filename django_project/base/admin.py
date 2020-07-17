"""Model admin class definitions.

Note these admin models inherit reversion (which provides history for a model).

..note:: if you add reversion.VersionAdmin to a model be sure to do
    ``./manage.py createinitialrevisions``.

.. see also:: https://github.com/etianen/django-reversion/wiki#getting
    -started-with-django-reversion

"""


from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from preferences.admin import PreferencesAdmin
from django.utils.translation import ugettext_lazy as _
import reversion
from .models import (
    Project,
    ProjectScreenshot,
    Domain,
    Organisation,
    SitePreferences,
    ProjectFlatpage
)
from .forms import ProjectFlatpageForm

admin.site.unregister(FlatPage)


class ProjectScreenshotAdmin(admin.TabularInline):
    """Admin for project's screenshot model."""

    model = ProjectScreenshot
    extra = 5


class ProjectAdmin(reversion.admin.VersionAdmin):
    """Admin for the project model."""

    filter_horizontal = (
        'certification_managers',
        'changelog_managers',
        'sponsorship_managers',
        'lesson_managers',)

    # Screenshot input in admin project panel.
    inlines = [ProjectScreenshotAdmin, ]

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class OrganisationAdmin(reversion.admin.VersionAdmin):
    """Admin for the organisation model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class ProjectFlatPageAdmin(admin.ModelAdmin):
    form = ProjectFlatpageForm
    fieldsets = (
        (None, {
            'fields': (
                'project', 'url', 'title', 'content', 'sites')
        }), (_(
            'Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments', 'registration_required', 'template_name')}),
    )
    list_display = ('url', 'title', 'project')
    list_filter = ('project', 'sites', 'registration_required')
    search_fields = ('url', 'title')


class GeneralFlatPageAdmin(FlatPageAdmin):
    def get_queryset(self, request):
        qs = super(FlatPageAdmin, self).get_queryset(request)
        project_flatpage_ids = (
            ProjectFlatpage.objects.all().values_list('id', flat=True))
        return qs.exclude(id__in=project_flatpage_ids)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Domain)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(SitePreferences, PreferencesAdmin)
admin.site.register(FlatPage, GeneralFlatPageAdmin)
admin.site.register(ProjectFlatpage, ProjectFlatPageAdmin)
