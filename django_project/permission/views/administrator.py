# -*- coding: utf-8 -*-
"""**View classes for Version**

"""

from braces.views import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import Http404
from django.views.generic import (
    CreateView,
    DeleteView
)
from permission.forms import ProjectAdministratorForm
from permission.models.project_administrator import ProjectAdministrator
from permission.views.user_manager import ProjectOwnerRequiredMixin

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '20/07/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class ProjectAdministratorCreateView(LoginRequiredMixin, ProjectOwnerRequiredMixin, CreateView):
    context_object_name = 'project_administrator'
    template_name = 'permission/administrator/create.html'
    form_class = ProjectAdministratorForm

    def get_form(self, form_class):
        form = super(ProjectAdministratorCreateView, self).get_form(form_class)
        return form

    def get_success_url(self):
        return reverse('user-manager', args=(self.request.user.username,))

    def get_form_kwargs(self):
        kwargs = super(ProjectAdministratorCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs.update({'project_slug': self.kwargs.get('project_slug', None)})
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(ProjectAdministratorCreateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Project by this name already exists!')


class ProjectAdministratorDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = 'administrator'
    template_name = 'permission/administrator/delete.html'

    def get_success_url(self):
        return reverse('user-manager', args=(self.request.user,))

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise Http404

        pk = self.kwargs.get('pk', None)
        try:
            project_administrator = ProjectAdministrator.objects.get(pk=pk)
            if project_administrator.project.owner != self.request.user:
                raise Http404("You don't have access to this page")
        except ProjectAdministrator.DoesNotExist:
            raise Http404

        return ProjectAdministrator.objects.all()
