"""Model admin class definitions.

Note these admin models inherit reversion (which provides history for a model).

..note:: if you add reversion.VersionAdmin to a model be sure to do
    ``./manage.py createinitialrevisions``.

.. see also:: https://github.com/etianen/django-reversion/wiki#getting
    -started-with-django-reversion

"""


from django.contrib import admin
from models import Project, ProjectScreenshots
import reversion


class ProjectScreenshotsAdmin(admin.TabularInline):
    model = ProjectScreenshots
    extra = 5


class ProjectAdmin(reversion.VersionAdmin):

    """Admin for the project model."""

    inlines = [ProjectScreenshotsAdmin, ]

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(Project, ProjectAdmin)
