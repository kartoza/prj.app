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
