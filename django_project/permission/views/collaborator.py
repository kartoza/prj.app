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
from permission.forms import ProjectCollaboratorForm
from permission.models.project_collaborator import ProjectCollaborator
from permission.views.user_manager import ProjectOwnerRequiredMixin

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '20/07/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class ProjectCollaboratorCreateView(LoginRequiredMixin, ProjectOwnerRequiredMixin, CreateView):
    context_object_name = 'project_collaborator'
    template_name = 'permission/collaborator/create.html'
    form_class = ProjectCollaboratorForm

    def get_form(self, form_class):
        form = super(ProjectCollaboratorCreateView, self).get_form(form_class)
        return form

    def get_success_url(self):
        return reverse('user-manager', args=(self.request.user.username,))

    def get_form_kwargs(self):
        kwargs = super(ProjectCollaboratorCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs.update({'project_slug': self.kwargs.get('project_slug', None)})
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(ProjectCollaboratorCreateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Project by this name already exists!')


class ProjectCollaboratorDeleteView(LoginRequiredMixin, ProjectOwnerRequiredMixin, DeleteView):
    context_object_name = 'collaborator'
    template_name = 'permission/collaborator/delete.html'

    def get_success_url(self):
        return reverse('user-manager', args=(self.request.user,))

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise Http404

        # checking permission
        pk = self.kwargs.get('pk', None)
        try:
            project_collaborator = ProjectCollaborator.objects.get(pk=pk)
            project = project_collaborator.project
            if not self.request.user.is_staff and project.owner != self.request.user:
                raise Http404("You don't have access to this page")
        except ProjectCollaborator.DoesNotExist:
            raise Http404

        return ProjectCollaborator.objects.all()
