# coding=utf-8
"""Forms for GeoContext app."""

from django import forms
from geocontext.models.context_service_registry import ContextServiceRegistry


def get_context_service_registry():
    service_registry_choices = [
        (m.name, m.display_name) for m in ContextServiceRegistry.objects.all()]
    return service_registry_choices


class GeoContextForm(forms.Form):
    x = forms.FloatField(label='X Coordinate', required=True)
    y = forms.FloatField(label='Y Coordinate', required=True)
    srid = forms.IntegerField(label='SRID')
    service_registry_name = forms.ChoiceField(
        label='Service Registry Name',
        required=True,
        choices=get_context_service_registry
    )
