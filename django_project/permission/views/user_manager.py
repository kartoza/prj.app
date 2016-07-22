# -*- coding: utf-8 -*-
"""**View classes for Version**

"""

from base.models import Project
from django.views.generic import (
    ListView)
from pure_pagination.mixins import PaginationMixin

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '20/07/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'
from braces.views._access import AccessMixin
from braces.views import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from permission.models.project_administrator import ProjectAdministrator


class ProjectAdministratorRequiredMixin(AccessMixin):
    """
    Mixin allows you to require a user with `is_staff` set to True.
    """

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return self.handle_no_permission(request)

        project_slug = self.kwargs.get('project_slug', None)
        if project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
                if not project.is_administrator(self.request.user):
                    raise Http404("You don't have access to this page")
            except Project.DoesNotExist:
                raise Http404

        return super(ProjectAdministratorRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class ProjectOwnerRequiredMixin(AccessMixin):
    """
    Mixin allows you to require a user with `is_staff` set to True.
    """

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return self.handle_no_permission(request)

        project_slug = self.kwargs.get('project_slug', None)
        if project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
                if project.owner != self.request.user:
                    raise Http404("You don't have access to this page")
            except Project.DoesNotExist:
                raise Http404

        return super(ProjectOwnerRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class UserManagerListView(PaginationMixin, LoginRequiredMixin, ListView):
    """List view for Version."""
    context_object_name = 'projects'
    template_name = 'permission/permission-list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(UserManagerListView, self).get_context_data(**kwargs)
        context['num_projects'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all project
        :rtype: QuerySet

        :raises: Http404
        """
        username = self.kwargs['username']
        if username != self.request.user.username:
            raise Http404
        if self.request.user.is_staff:
            project_qs = Project.objects.all()
        else:
            projects_in_admin = ProjectAdministrator.objects.filter(user=self.request.user).values('project')
            project_qs = Project.objects.filter(Q(owner=self.request.user) | Q(pk__in=projects_in_admin))
        return project_qs
