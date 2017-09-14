# coding=utf-8
import logging
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from models import Project

logger = logging.getLogger(__name__)


class ProjectForm(forms.ModelForm):
    """Form for creating projects."""

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class."""
        model = Project
        fields = (
            'name',
            'image_file',
            'gitter_room',
            'signature',
            'credit_cost',
            'certificate_credit',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                'Project details',
                Field('name', css_class="form-control"),
                Field('image_file', css_class="form-control"),
                Field('signature', css_class="form-control"),
                Field('credit_cost', css_class="form-control"),
                Field('certificate_credit', css_class="form-control"),
                Field('gitter_room', css_class="form-control"),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(ProjectForm, self).save(commit=False)
        instance.owner = self.user
        instance.save()
        return instance


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        label='First Name (Optional)',
        required=False,
        widget=forms.TextInput(
            {
                "placeholder": _('First Name')
            })
    )

    last_name = forms.CharField(
        max_length=150,
        label='Last Name (Optional)',
        required=False,
        widget=forms.TextInput(
            {
                "placeholder": _('Last Name')
            })
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
