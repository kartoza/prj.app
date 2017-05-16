# coding=utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.admin import widgets
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
    CourseConvener,
    CourseType,
    Course,
    TrainingCenter,
)


class CustomSelectMultipleWidget(widgets.FilteredSelectMultiple):

    class Media:
        css = {'all': ['/static/css/custom-widget.css',
                       '/static/grappelli/jquery/ui/jquery-ui.min.css',
                       '/static/grappelli/stylesheets/screen.css']}


class CertifyingOrganisationForm(forms.ModelForm):

    organisation_owners = forms.ModelMultipleChoiceField(
        queryset=User.objects.order_by('username'),
        widget=CustomSelectMultipleWidget("user", is_stacked=False),
    )

    # noinspection PyClassicStyleClass.
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
                Field('organisation_owners', css_class='form-control'),
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


class CourseTypeForm(forms.ModelForm):

    # noinspection PyClassicStyleClass.
    class Meta:
        model = CourseType
        fields = (
            'name',
            'description',
            'instruction_hours',
            'coursetype_link',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.certifying_organisation = kwargs.pop('certifying_organisation')
        form_title = \
            'New Course Type for %s' % self.certifying_organisation.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('description', css_class='form-control'),
                Field('instruction_hours', css_class='form-control'),
                Field('coursetype_link', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CourseTypeForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CourseTypeForm, self).save(commit=False)
        instance.certifying_organisation = self.certifying_organisation
        instance.author = self.user
        instance.save()
        return instance


class CourseConvenerForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        queryset=User.objects.order_by('username'),
        widget=forms.Select)

    # noinspection PyClassicStyleClass.
    class Meta:
        model = CourseConvener
        fields = (
            'user',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.certifying_organisation = kwargs.pop('certifying_organisation')
        form_title = 'New Course Convener for %s' % \
                     self.certifying_organisation.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('user', css_class='form-control'),)
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CourseConvenerForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CourseConvenerForm, self).save(commit=False)
        instance.certifying_organisation = self.certifying_organisation
        instance.save()
        return instance


class CourseForm(forms.ModelForm):

    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'datepicker'}))

    # noinspection PyClassicStyleClass.
    class Meta:
        model = Course
        fields = (
            'course_type',
            'course_convener',
            'training_center',
            'start_date',
            'end_date',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.certifying_organisation = kwargs.pop('certifying_organisation')
        form_title = 'New Course for %s' % self.certifying_organisation.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('course_type', css_class='form-control'),
                Field('course_convener', css_class='form-control'),
                Field('training_center', css_class='form-control'),
                Field('start_date'),
                Field('end_date'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['course_convener'].queryset = \
            CourseConvener.objects.filter(
                certifying_organisation=self.certifying_organisation)
        self.fields['course_type'].queryset = \
            CourseType.objects.filter(
                certifying_organisation=self.certifying_organisation)
        self.fields['training_center'].queryset = \
            TrainingCenter.objects.filter(
                certifying_organisation=self.certifying_organisation)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CourseForm, self).save(commit=False)
        instance.certifying_organisation = self.certifying_organisation
        instance.author = self.user
        instance.save()
        return instance
