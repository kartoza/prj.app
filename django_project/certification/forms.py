# coding=utf-8
from __future__ import unicode_literals
import json
import os
from django import forms
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.contrib.gis import forms as geoforms
from django.contrib.gis import gdal
from django.contrib.gis.forms.widgets import BaseGeometryWidget
from django.core.exceptions import ValidationError
from django.contrib.gis.forms.widgets import OSMWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from .models import (
    CertifyingOrganisation,
    CertificateType,
    CourseConvener,
    CourseType,
    TrainingCenter,
    Course,
    CourseAttendee,
    Attendee,
    Certificate,
    CertifyingOrganisationCertificate, Checklist, OrganisationChecklist
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
            'url',
            'address',
            'country',
            'organisation_phone',
            'logo',
            'owner_message',
            'organisation_owners',
            'project',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = kwargs.pop('form_title', None)
        show_owner_message = kwargs.pop('show_owner_message', None)
        if not form_title:
            form_title = (
                'New Certifying Organisation for %s' % self.project
            )
        self.helper = FormHelper()
        self.helper.include_media = False
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('organisation_email', css_class='form-control'),
                Field('url', css_class='form-control'),
                Field('address', css_class='form-control'),
                Field('country', css_class='form-control chosen-select'),
                Field('organisation_phone', css_class='form-control'),
                Field('logo', css_class='form-control'),
                Field('owner_message', css_class='form-control'),
                Field('organisation_owners', css_class='form-control'),
                Field('project', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CertifyingOrganisationForm, self).__init__(*args, **kwargs)
        self.fields['organisation_owners'].label_from_instance = \
            lambda obj: "%s <%s>" % (obj.get_full_name(), obj)
        self.fields['organisation_owners'].initial = [self.user]
        self.fields['project'].initial = self.project
        self.fields['project'].widget = forms.HiddenInput()
        if show_owner_message:
            self.fields['owner_message'].label = (
                'Message to validator'
            )
            self.fields['owner_message'].help_text = ''
        else:
            self.fields['owner_message'].widget = (
                forms.HiddenInput()
            )
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CertifyingOrganisationForm, self).save(commit=False)

        if (
            not instance.approved and
                instance.status and
                instance.status.name.lower() == 'pending'
        ):
            if instance.owner_message:
                instance.status = None
                instance.remarks = ''

        instance.save()
        self.save_m2m()

        # Check checklist
        checklist_data = {}
        for key, value in self.data.items():
            checklist_id = ''
            if 'checklist-' in key:
                checklist_id = key.split('-')[1]
                if checklist_id not in checklist_data:
                    checklist_data[checklist_id] = {}
                checklist_data[checklist_id]['checked'] = (
                    True if value == 'yes' else False
                )
            if 'textarea-' in key:
                checklist_id = key.split('-')[1]
                if checklist_id not in checklist_data:
                    checklist_data[checklist_id] = {}
                checklist_data[checklist_id]['text'] = (
                    value
                )
            if checklist_id:
                checklist = Checklist.objects.get(
                    id=checklist_id
                )
                checklist_data[checklist_id]['question'] = (
                    checklist.question
                )
        for key, value in checklist_data.items():
            checklist = Checklist.objects.get(id=key)
            organisation = CertifyingOrganisation.objects.get(
                id=instance.id
            )
            org_checklist, created = (
                OrganisationChecklist.objects.get_or_create(
                    organisation=organisation,
                    checklist=checklist
                )
            )
            if created:
                org_checklist.submitter = self.user
                org_checklist.checklist_question = value['question']
                org_checklist.checklist_target = checklist.target

            org_checklist.checked = value['checked']
            if 'text' in value:
                org_checklist.text_box_content = value['text']
            org_checklist.save()

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
            'certifying_organisation',
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
        self.fields['certifying_organisation'].initial = \
            self.certifying_organisation
        self.fields['certifying_organisation'].widget = forms.HiddenInput()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CourseTypeForm, self).save(commit=False)
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
            'title',
            'user',
            'degree',
            'signature',
            'is_active',
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
                Field('title', css_class='form-control'),
                Field('user', css_class='form-control chosen-select'),
                Field('degree', css_class='form-control'),
                Field('signature', css_class='form-control'),
                Field('is_active', css_class='checkbox-primary'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CourseConvenerForm, self).__init__(*args, **kwargs)
        self.fields['user'].label_from_instance = \
            lambda obj: "%s < %s >" % (obj.get_full_name(), obj)
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
            '/static/js/libs/OpenLayers-2.13.1/OpenLayers.js',
            '/static/js/libs/OpenLayers-2.13.1/OpenStreetMapSSL.js',
        )

    def __init__(self, attrs=None):
        super(CustomOSMWidget, self).__init__()
        for key in ('default_lon', 'default_lat'):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)
        self.attrs['default_zoom'] = 10

    @property
    def map_srid(self):
        # Use the official spherical mercator projection SRID when GDAL is
        # available.
        if gdal.GDAL_VERSION:
            return 3857
        else:
            return 4326


class TrainingCenterForm(geoforms.ModelForm):

    location = geoforms.PointField(widget=OSMWidget(
        attrs={
            'map_width': 750,
            'map_height': 400,
            'default_zoom': 5,
            'default_lat': -30.559482,
            'default_lon': 22.937506
        }), required=False)

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

        json_file = settings.STATIC_ROOT + '/json/geo.json'
        found = os.path.exists(json_file)
        lat = -30.559482
        lon = 22.937506
        if found:
            with open(json_file) as file:
                datas = json.load(file)
                for data in datas['features']:
                    if data['properties'][
                            'ISO2'] == self.certifying_organisation.country:
                        lat = data['properties']['LAT']
                        lon = data['properties']['LON']
        point = Point(x=lon, y=lat, srid=4326)
        self.fields['location'].initial = point
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
            'language',
            'trained_competence',
            'start_date',
            'end_date',
            'template_certificate',
            'certifying_organisation',
            'certificate_type',
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
                Field('language', css_class='form-control'),
                Field('trained_competence', css_class='form-control'),
                Field('start_date', css_class='form-control'),
                Field('end_date', css_class='form-control'),
                Field('template_certificate', css_class='form-control'),
                Field('certificate_type', css_class='form-control'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['course_convener'].queryset = \
            CourseConvener.objects.filter(
                certifying_organisation=self.certifying_organisation,
                is_active=True)
        self.fields['course_convener'].label_from_instance = \
            lambda obj: "%s <%s>" % (obj.user.get_full_name(), obj)
        self.fields['course_type'].queryset = \
            CourseType.objects.filter(
                certifying_organisation=self.certifying_organisation)
        self.fields['training_center'].queryset = \
            TrainingCenter.objects.filter(
                certifying_organisation=self.certifying_organisation)
        self.fields['certifying_organisation'].initial = \
            self.certifying_organisation
        self.fields['certifying_organisation'].widget = forms.HiddenInput()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['certificate_type'].queryset = \
            CertificateType.objects.filter(
                projectcertificatetype__project=
                self.certifying_organisation.project)

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
        widgets = {'course': forms.HiddenInput()}

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

    add_to_course = forms.BooleanField(
        initial=True,
        help_text='Add this attendee to course.',
        required=False
    )

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
                Field('add_to_course', css_class='form-control')
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
        instance.save()
        return instance


class UpdateAttendeeForm(forms.ModelForm):

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
        form_title = 'Update Attendee'
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
        super(UpdateAttendeeForm, self).__init__(*args, **kwargs)
        self.fields['certifying_organisation'].initial = \
            self.certifying_organisation
        self.fields['certifying_organisation'].widget = forms.HiddenInput()
        self.helper.add_input(Submit('submit', 'Add'))

    def save(self, commit=True):
        instance = super(UpdateAttendeeForm, self).save(commit=False)
        instance.author = self.user
        instance.save()
        return instance


class CertificateForm(forms.ModelForm):

    class Meta:
        model = Certificate
        fields = (
            'course',
            'attendee',
            'certificate_type',
            'is_paid',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.course = kwargs.pop('course')
        self.attendee = kwargs.pop('attendee')
        self.certificate_type = kwargs.pop('certificate_type')
        organisation_credits = \
            self.course.certifying_organisation.organisation_credits
        cost = self.course.certifying_organisation.project.certificate_credit
        remaining_credits = organisation_credits - cost
        self.helper = FormHelper()
        self.helper.html5_required = False
        super(CertificateForm, self).__init__(*args, **kwargs)
        self.fields['course'].initial = self.course
        self.fields['course'].widget = forms.HiddenInput()
        self.fields['attendee'].initial = self.attendee
        self.fields['attendee'].widget = forms.HiddenInput()
        self.fields['certificate_type'].initial = self.certificate_type
        self.fields['certificate_type'].widget = forms.HiddenInput()
        if remaining_credits >= 0:
            self.fields['is_paid'].initial = True
        else:
            self.fields['is_paid'].initial = False
        self.fields['is_paid'].widget = forms.HiddenInput()
        self.helper.add_input(Submit('submit', 'Issue Certificate'))

    def clean(self):
        clean_data = self.cleaned_data
        organisation = self.course.certifying_organisation

        remaining_credits = \
            organisation.organisation_credits - \
            organisation.project.certificate_credit

        if remaining_credits < 0:
            raise ValidationError("Insufficient credits")

        return clean_data

    def save(self, commit=True):
        instance = super(CertificateForm, self).save(commit=False)
        instance.author = self.user
        instance.course = self.course
        instance.attendee = self.attendee
        instance.certificate_type = self.certificate_type
        instance.save()
        return instance


class CsvAttendeeForm(forms.Form):
    """Form to upload CSV file."""

    file = forms.FileField(
        label="Choose Attendee CSV File:",
        widget=forms.FileInput(
            attrs={
                'accept': ".csv"
            }
        )
    )


class OrganisationCertificateForm(forms.ModelForm):

    class Meta:
        model = CertifyingOrganisationCertificate
        fields = (
            'certifying_organisation',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.certifying_organisation = kwargs.pop('certifying_organisation')
        self.helper = FormHelper()
        self.helper.html5_required = False
        super(OrganisationCertificateForm, self).__init__(*args, **kwargs)
        self.fields['certifying_organisation'].initial = \
            self.certifying_organisation
        self.fields['certifying_organisation'].widget = forms.HiddenInput()
        self.helper.add_input(Submit('submit', 'Issue Certificate'))

    def save(self, commit=True):
        instance = super(OrganisationCertificateForm, self).save(commit=False)
        instance.author = self.user
        instance.save()
        return instance
