# -*- coding: utf-8 -*-
"""**View classes for Version**

"""

from base.models import Project
from braces.views import LoginRequiredMixin
from django.http import Http404
from django.views.generic import (
    ListView)
from pure_pagination.mixins import PaginationMixin

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '20/07/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


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
        if not self.request.user.is_authenticated():
            raise Http404
        username = self.kwargs['username']
        if username != self.request.user.username:
            raise Http404
        if self.request.user.is_staff:
            project_qs = Project.objects.all()
        else:
            project_qs = Project.objects.filter(owner=self.request.user)
        return project_qs
