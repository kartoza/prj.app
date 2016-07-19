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
from models import ProjectAdministrator, ProjectCollaborator
from forms import ProjectAdministratorForm, ProjectCollaboratorForm
import reversion


class ProjectAdministratorAdmin(reversion.VersionAdmin):
    """Category admin model."""
    form = ProjectAdministratorForm

    def get_form(self, request, *args, **kwargs):
        form = super(ProjectAdministratorAdmin, self).get_form(request, *args, **kwargs)
        form.user = request.user
        form.base_fields['project'].widget.can_add_related = False
        form.base_fields['user'].widget.can_add_related = False
        return form

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class ProjectCollaboratorAdmin(reversion.VersionAdmin):
    """Category admin model."""
    form = ProjectCollaboratorForm

    def get_form(self, request, *args, **kwargs):
        form = super(ProjectCollaboratorAdmin, self).get_form(request, *args, **kwargs)
        form.user = request.user
        form.base_fields['project'].widget.can_add_related = False
        form.base_fields['user'].widget.can_add_related = False
        return form

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(ProjectAdministrator, ProjectAdministratorAdmin)
admin.site.register(ProjectCollaborator, ProjectCollaboratorAdmin)
