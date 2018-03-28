# coding=utf-8
"""Context Service Registry Model."""

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ContextServiceRegistry(models.Model):
    """Context Service Registry"""

    WFS = 'wfs'
    WCS = 'wcs'
    WMS = 'wms'
    REST = 'rest'
    WIKIPEDIA = 'wikipedia'
    QUERY_TYPES = (
        (WFS, 'WFS'),
        (WCS, 'WCS'),
        (WMS, 'WMS'),
        (REST, 'REST'),
        (WIKIPEDIA, 'Wikipedia'),
    )

    name = models.CharField(
        help_text=_('Name of Context Service.'),
        blank=False,
        null=False,
        max_length=200,
    )

    display_name = models.CharField(
        help_text=_('Display Name of Context Service.'),
        blank=False,
        null=False,
        max_length=200,
    )

    description = models.CharField(
        help_text=_('Description of Context Service.'),
        blank=False,
        null=False,
        max_length=1000,
    )

    url = models.CharField(
        help_text=_('URL of Context Service.'),
        blank=False,
        null=False,
        max_length=1000,
    )

    user = models.CharField(
        help_text=_('User name for accessing Context Service.'),
        blank=True,
        null=False,
        max_length=200,
    )

    password = models.CharField(
        help_text=_('Password for accessing Context Service.'),
        blank=True,
        null=False,
        max_length=200,
    )

    api_key = models.CharField(
        help_text=_('API key for accessing Context Service.'),
        blank=True,
        null=False,
        max_length=200,
    )

    query_url = models.CharField(
        help_text=_('Query URL for accessing Context Service.'),
        blank=False,
        null=False,
        max_length=1000,
    )

    query_type = models.CharField(
        help_text=_('Query type of the Context Service.'),
        blank=True,
        null=False,
        max_length=200,
        choices=QUERY_TYPES
    )

    # I will try to use CharField first, if not I will use django-regex-field
    result_regex = models.CharField(
        help_text=_('Regex to retrieve the desired value.'),
        blank=True,
        null=False,
        max_length=200,
    )

    time_to_live = models.IntegerField(
        help_text=_('Time to live of Context Service to be used in caching.'),
        blank=True,
        null=False,
    )
