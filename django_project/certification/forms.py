# coding=utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.contrib.gis import forms as geoforms
from django.contrib.gis import gdal
from django.contrib.gis.forms.widgets import BaseGeometryWidget
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
    TrainingCenter,
    Course,
    CourseAttendee,
    Attendee,
    Certificate,
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
            'logo',
            'organisation_owners',
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
                Field('logo', css_class='form-control'),
                Field('organisation_owners', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CertifyingOrganisationForm, self).__init__(*args, **kwargs)
        self.fields['organisation_owners'].label_from_instance = \
            lambda obj: "%s <%s>" % (obj.get_full_name(), obj)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CertifyingOrganisationForm, self).save(commit=False)
        instance.project = self.project
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
            'signature',
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
                Field('user', css_class='form-control chosen-select'),
                Field('signature', css_class='form-control'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CourseConvenerForm, self).__init__(*args, **kwargs)
        self.fields['user'].label_from_instance = \
            lambda obj: "%s <%s>" % (obj.get_full_name(), obj)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CourseConvenerForm, self).save(commit=False)
        instance.certifying_organisation = self.certifying_organisation
        instance.save()
        return instance


class CustomOSMWidget(BaseGeometryWidget):
    """An OpenLayers/OpenStreetMap-based widget."""

    template_name = 'gis/openlayers-osm.html'

    default_lon = 0
    default_lat = 0

    class Media:
        css = {'all': ['/static/css/custom-widget.css',
                       '/static/grappelli/jquery/ui/jquery-ui.min.css',
                       '/static/grappelli/stylesheets/screen.css']}

        js = (
            '/en/site-admin/jsi18n/',
            '/static/grappelli/jquery/jquery-2.1.4.min.js',
            '/static/grappelli/jquery/ui/jquery-ui.min.js',
            '/static/grappelli/js/grappelli.js',
            '/static/admin/js/SelectBox.js',
            '/static/admin/js/SelectFilter2.js',
            '/static/js/libs/OpenLayers-2.13.1/OpenLayers.js',
            '/static/js/libs/OpenLayers-2.13.1/OpenStreetMapSSL.js',
            '/static/gis/js/OLMapWidget.js'
        )

    def __init__(self, attrs=None):
        super(CustomOSMWidget, self).__init__()
        for key in ('default_lon', 'default_lat'):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)

    @property
    def map_srid(self):
        # Use the official spherical mercator projection SRID when GDAL is
        # available.
        if gdal.HAS_GDAL:
            return 3857
        else:
            return 4326


class TrainingCenterForm(geoforms.ModelForm):

    location = geoforms.PointField(widget=CustomOSMWidget(
        attrs={'map_width': 600, 'map_height': 400}), )

    class Meta:
        model = TrainingCenter
        fields = (
            'name',
            'email',
            'address',
            'phone',
            'location',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.certifying_organisation = kwargs.pop('certifying_organisation')
        form_title = 'New Training Center for %s' % \
                     self.certifying_organisation.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('email', css_class='form-control'),
                Field('address', css_class='form-control'),
                Field('phone', css_class='form-control'),
                Field('location', css_class='form-control'),
            ))
        self.helper.layout = layout
        self.helper.html5_required = False
        super(TrainingCenterForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(TrainingCenterForm, self).save(commit=False)
        instance.certifying_organisation = self.certifying_organisation
        instance.author = self.user
        instance.save()
        return instance


class CourseForm(forms.ModelForm):

    # noinspection PyClassicStyleClass.
    class Meta:
        model = Course
        fields = (
            'course_type',
            'course_convener',
            'training_center',
            'start_date',
            'end_date',
            'template_certificate'
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
                Field('course_convener',
                      css_class='form-control chosen-select'),
                Field('training_center', css_class='form-control'),
                Field('start_date', css_class='form-control'),
                Field('end_date', css_class='form-control'),
                Field('template_certificate', css_class='form-control'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['course_convener'].queryset = \
            CourseConvener.objects.filter(
                certifying_organisation=self.certifying_organisation)
        self.fields['course_convener'].label_from_instance = \
            lambda obj: "%s <%s>" % (obj.user.get_full_name(), obj)
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


class CourseAttendeeForm(forms.ModelForm):

    class Meta:
        model = CourseAttendee
        fields = ('attendee', 'course')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.course = kwargs.pop('course')
        self.certifying_organisation = kwargs.pop('certifying_organisation')
        form_title = 'Add Course Attendee'
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('attendee', css_class='form-control chosen-select'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CourseAttendeeForm, self).__init__(*args, **kwargs)
        self.fields['attendee'].queryset = \
            Attendee.objects.filter(
                certifying_organisation=self.certifying_organisation)
        self.fields['course'].initial = self.course
        self.fields['course'].widget = forms.HiddenInput()
        self.helper.add_input(Submit('submit', 'Add'))

    def save(self, commit=True):
        instance = super(CourseAttendeeForm, self).save(commit=False)
        instance.author = self.user
        instance.save()
        return instance


class AttendeeForm(forms.ModelForm):

    class Meta:
        model = Attendee
        fields = (
            'firstname',
            'surname',
            'email',
            'certifying_organisation',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.certifying_organisation = kwargs.pop('certifying_organisation')
        form_title = 'Add Attendee'
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('firstname', css_class='form-control'),
                Field('surname', css_class='form-control'),
                Field('email', css_class='form-control'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(AttendeeForm, self).__init__(*args, **kwargs)
        self.fields['certifying_organisation'].initial = \
            self.certifying_organisation
        self.fields['certifying_organisation'].widget = forms.HiddenInput()
        self.helper.add_input(Submit('submit', 'Add'))

    def save(self, commit=True):
        instance = super(AttendeeForm, self).save(commit=False)
        instance.author = self.user
        instance.certifying_organisation = self.certifying_organisation
        instance.save()
        return instance


class CertificateForm(forms.ModelForm):

    class Meta:
        model = Certificate
        fields = (
            'course',
            'attendee',
            'cost',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.course = kwargs.pop('course')
        self.attendee = kwargs.pop('attendee')
        certificate_all = Certificate.objects.filter(course=self.course)
        cost_value = 0
        for certificate in certificate_all:
            if certificate.cost:
                cost_value = certificate.cost
        self.helper = FormHelper()
        self.helper.html5_required = False
        super(CertificateForm, self).__init__(*args, **kwargs)
        self.fields['course'].initial = self.course
        self.fields['course'].widget = forms.HiddenInput()
        self.fields['attendee'].initial = self.attendee
        self.fields['attendee'].widget = forms.HiddenInput()
        self.fields['cost'].initial = cost_value
        self.fields['cost'].widget = forms.HiddenInput()
        self.helper.add_input(Submit('submit', 'Add'))

    def save(self, commit=True):
        instance = super(CertificateForm, self).save(commit=False)
        instance.author = self.user
        instance.course = self.course
        instance.attendee = self.attendee
        instance.save()
        return instance
