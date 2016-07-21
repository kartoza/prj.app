# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/07/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from base.models.project import Project
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import SuspiciousOperation
from models import (
    ProjectAdministrator,
    ProjectCollaborator
)


class ProjectAdministratorForm(forms.ModelForm):
    # noinspection PyClassicStyleClass
    class Meta:
        model = ProjectAdministrator
        fields = ('project', 'user')

    def __init__(self, *args, **kwargs):
        try:
            self.user
        except AttributeError:
            self.user = kwargs.pop('user')

        if not self.user:
            raise Http404
        self.helper = FormHelper()
        form_title = 'Assign Administrator'
        layout = Layout(
            Fieldset(
                form_title,
                Field('project', css_class='form-control'),
                Field('user', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False

        # init choice
        self.project = None
        try:
            self.project_slug = kwargs.pop('project_slug')
            self.project = Project.objects.get(slug=self.project_slug)
        except AttributeError:
            pass
        except Project.DoesNotExist:
            pass

        super(ProjectAdministratorForm, self).__init__(*args, **kwargs)

        # init choice
        self.helper.add_input(Submit('submit', 'Submit'))
        users = User.objects.exclude(username=self.user).order_by('username')
        if self.user.is_staff:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(owner=self.user)
        self.fields["user"].queryset = users
        self.fields["project"].queryset = projects

        # assign initial project
        if self.project:
            self.initial['project'] = self.project

    def clean(self):
        cleaned_data = super(ProjectAdministratorForm, self).clean()
        project = cleaned_data.get("project")
        try:
            project = Project.objects.get(name=project)
            if not self.user.is_staff and not project.owner == self.user:
                raise SuspiciousOperation
        except Project.DoesNotExist:
            raise SuspiciousOperation


class ProjectCollaboratorForm(forms.ModelForm):
    # noinspection PyClassicStyleClass
    class Meta:
        model = ProjectCollaborator
        fields = ('project', 'user')

    def __init__(self, *args, **kwargs):
        try:
            self.user
        except AttributeError:
            self.user = kwargs.pop('user')

        if not self.user:
            raise Http404
        self.helper = FormHelper()
        form_title = 'Assign Collaborator'
        layout = Layout(
            Fieldset(
                form_title,
                Field('project', css_class='form-control'),
                Field('user', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False

        # init choice
        self.project = None
        try:
            self.project_slug = kwargs.pop('project_slug')
            self.project = Project.objects.get(slug=self.project_slug)
        except AttributeError:
            pass
        except Project.DoesNotExist:
            pass

        super(ProjectCollaboratorForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

        # init choice
        users = User.objects.exclude(username=self.user).order_by('username')
        if self.user.is_staff:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(owner=self.user)
        self.fields["user"].queryset = users
        self.fields["project"].queryset = projects

        # assign initial project
        if self.project:
            self.initial['project'] = self.project

    def clean(self):
        cleaned_data = super(ProjectCollaboratorForm, self).clean()
        project = cleaned_data.get("project")
        try:
            project = Project.objects.get(name=project)
            if not self.user.is_staff and not project.owner == self.user:
                raise SuspiciousOperation
        except Project.DoesNotExist:
            raise SuspiciousOperation
