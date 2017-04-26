# coding=utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.admin import widgets
from django.contrib.admin import options
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from models import (
    CertifyingOrganisation,
)


class CertifyingOrganisationForm(forms.ModelForm):

    organisation_owners = forms.ModelMultipleChoiceField(
        widget=widgets.FilteredSelectMultiple("user", is_stacked=False),
        queryset=User.objects.order_by('username'),
    )

    options.BaseModelAdmin.filter_horizontal = ('organisation_owners',)

    # noinspection PyClassicStyleClass
    class Meta:
        model = CertifyingOrganisation
        fields = (
            'name',
            'organisation_email',
            'address',
            'country',
            'organisation_phone',
            'organisation_owners'
        )

    class Media:
        css = {'all': ('/media/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'New Certifying Organisation for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('organisation_email', css_class='form-control'),
                Field('address', css_class='form-control'),
                Field('country', css_class='form-control chosen-select'),
                Field('organisation_phone', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CertifyingOrganisationForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CertifyingOrganisationForm, self).save(commit=False)
        instance.project = self.project
        instance.approved = False
        instance.save()
        self.save_m2m()
        return instance
