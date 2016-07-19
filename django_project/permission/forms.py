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
        if not self.user:
            raise Http404
        self.helper = FormHelper()
        form_title = 'assign administrator'
        layout = Layout(
            Fieldset(
                form_title,
                Field('project', css_class='form-control'),
                Field('user', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False

        super(ProjectAdministratorForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

        # init choice
        users = User.objects.exclude(username=self.user)
        projects = Project.objects.filter(owner=self.user)
        self.fields["user"].queryset = users
        self.fields["project"].queryset = projects


class ProjectCollaboratorForm(forms.ModelForm):
    # noinspection PyClassicStyleClass
    class Meta:
        model = ProjectCollaborator
        fields = ('project', 'user')

    def __init__(self, *args, **kwargs):
        if not self.user:
            raise Http404
        self.helper = FormHelper()
        form_title = 'assign collaborator'
        layout = Layout(
            Fieldset(
                form_title,
                Field('project', css_class='form-control'),
                Field('user', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False

        super(ProjectCollaboratorForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

        # init choice
        users = User.objects.exclude(username=self.user)
        projects = Project.objects.filter(owner=self.user)
        self.fields["user"].queryset = users
        self.fields["project"].queryset = projects
