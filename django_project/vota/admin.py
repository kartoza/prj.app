# coding=utf-8
"""Model admin class definitions.

Note these admin models inherit both AuditedAdmin (which adds owner, editor,
creation date, modification date to a model) and reversion (which provides
historisation for a model).

..note:: if you add reversion.VersionAdmin to a model be sure to do
    ``./manage.py createinitialrevisions``.

.. see also:: https://github.com/etianen/django-reversion/wiki#getting
    -started-with-django-reversion

"""


from django.contrib import admin
from models import Committee, Vote, Ballot
from audited_models.admin import AuditedAdmin
import reversion


class CommitteeAdmin(AuditedAdmin, reversion.VersionAdmin):
    """Committee admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class VoteAdmin(AuditedAdmin, reversion.VersionAdmin):
    """Vote admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class BallotAdmin(AuditedAdmin, reversion.VersionAdmin):
    """Ballot admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Ballot, BallotAdmin)
