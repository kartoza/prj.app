# coding=utf-8
"""Context Service Registry Model."""

import requests
from xml.dom import minidom

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
        null=True,
    )

    def retrieve_context_value(self, x, y):
        # construct bbox
        bbox = [x, y, x * (1.0001), y * (1.0001)]
        bbox_string = ','.join([str(i) for i in bbox])
        url = self.query_url + '&BBOX=' + bbox_string
        print(url)
        request = requests.get(url)
        content = request.content
        return self.parse_request_content(content)

    def parse_request_content(self, request_content):
        if self.query_type == self.WFS:
            xmldoc = minidom.parseString(request_content)
            provname_dom = xmldoc.getElementsByTagName(self.result_regex)[0]
            return provname_dom.childNodes[0].nodeValue
