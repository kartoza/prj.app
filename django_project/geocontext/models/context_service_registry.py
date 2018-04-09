# coding=utf-8
"""Context Service Registry Model."""

import requests
from xml.dom import minidom

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.http import QueryDict

from geocontext.utilities import convert_coordinate, parse_gml_geometry


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

    crs = models.IntegerField(
        help_text=_('The CRS of the context service registry in EPSG code.'),
        blank=True,
        null=True,
        default=4326
    )

    layer_typename = models.CharField(
        help_text=_('Layer type name to get the context.'),
        blank=False,
        null=False,
        max_length=200,
    )

    service_version = models.CharField(
        help_text=_('Version of the service (e.g. WMS 1.1.0, WFS 2.0.0).'),
        blank=False,
        null=False,
        max_length=200,
    )

    def retrieve_context_value(self, x, y, crs=4326):
        """Retrieve context from a location.

        :param x: The value of x coordinate.
        :type x: float

        :param y: The value of y coordinate.
        :type y: float

        :param crs: The crs of the coordinate.
        :type crs: int
        """
        url = self.build_query_url(x, y, crs)
        request = requests.get(url)
        content = request.content
        geometry = parse_gml_geometry(content)
        value = self.parse_request_value(content)

        # Create cache here.

        return geometry, value

    def parse_request_value(self, request_content):
        """Parse request value from request content.

        :param request_content: String that represent content of a request.
        :type request_content: unicode

        :returns: The value of the result_regex in the request_content.
        :rtype: unicode
        """
        if self.query_type == ContextServiceRegistry.WFS:
            xmldoc = minidom.parseString(request_content)
            try:
                value_dom = xmldoc.getElementsByTagName(self.result_regex)[0]
                return value_dom.childNodes[0].nodeValue
            except IndexError:
                return None

    def build_query_url(self, x, y, crs=4326):
        """Build query based on the model and the parameter.

        :param x: The value of x coordinate.
        :type x: float

        :param y: The value of y coordinate.
        :type y: float

        :param crs: The crs of the coordinate.
        :type crs: int

        :return: URL to do query.
        :rtype: unicode
        """
        if self.query_type == ContextServiceRegistry.WFS:
            # construct bbox
            if crs != self.crs:
                x, y = convert_coordinate(x, y, crs, self.crs)
            x_pair = x * 1.0001
            y_pair = y * 1.0001
            if x < x_pair:
                if y < y_pair:
                    bbox = [x, y, x_pair, y_pair]
                else:
                    bbox = [x, y_pair, x_pair, y]
            else:
                if y < y_pair:
                    bbox = [x_pair, y, x, y_pair]
                else:
                    bbox = [x_pair, y_pair, x, y]

            bbox_string = ','.join([str(i) for i in bbox])

            parameters = {
                'SERVICE': 'WFS',
                'REQUEST': 'GetFeature',
                'VERSION': self.service_version,
                'TYPENAME': self.layer_typename,
                # 'SRSNAME': 'EPSG:%s' % self.crs,  # added manually
                'OUTPUTFORMAT': 'GML3',
                # 'BBOX': bbox_string  # added manually
            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(parameters)

            if '?' in self.url:
                url = self.url + '&' + query_dict.urlencode()
            else:
                url = self.url + '?' + query_dict.urlencode()
            url += '&SRSNAME=%s' % self.crs
            url += '&BBOX=' + bbox_string

            return url
