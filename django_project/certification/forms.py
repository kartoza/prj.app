# coding=utf-8
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from models import (
    TrainingCenter,
    CertifyingOrganisation
)


class CertifyingOrganisationForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = CertifyingOrganisation
        fields = (
            'name',
            'address',
            'organisation_email',
            'organisation_phone',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'New Certifying Organisation for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('address', css_class='form-control'),
                Field('organisation_email', css_class='form-control'),
                Field('organisation_phone', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CertifyingOrganisationForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CertifyingOrganisationForm, self).save(commit=False)
        instance.author = self.user
        instance.project = self.project
        instance.approved = False
        instance.save()
        return instance


class TrainingCenterForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = TrainingCenter
        fields = (
            'name',
            'email',
            'address',
            'phone'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        self.certifying_organisation = kwargs.pop('certifying_organisation')
        form_title = 'New Training Center for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('email', css_class='form-control'),
                Field('address', css_class='form-control'),
                Field('phone', css_class='phone'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(TrainingCenterForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(TrainingCenterForm, self).save(commit=False)
        instance.author = self.user
        instance.project = self.project
        instance.certifying_organisation = self.certifying_organisation
        instance.approved = False
        instance.save()
        return instance
