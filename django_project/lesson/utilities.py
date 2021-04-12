# coding=utf-8
"""Tools for the lesson app."""

import json
import re
import requests

from unidecode import unidecode
from urllib.parse import urlparse

from django.http import Http404, HttpResponse
from django.urls import reverse
from django.utils.text import slugify

from core.settings.contrib import STOP_WORDS


def custom_slug(name):
    """Slugify a string with our own rules.

    :param name: The name or title to slugify.
    :type name: basestring

    :return: The new slug.
    :rtype: basestring
    """
    words = name.split()
    filtered_words = [
        word for word in words if word.lower() not in STOP_WORDS]
    # unidecode() represents special characters (unicode data) in ASCII
    new_list = unidecode(' '.join(filtered_words))
    new_slug = slugify(new_list)[:50]
    return new_slug


def re_order_features(request, features):
    """Helper to reorder a set of features.

    The column must be called `sequence_number` in your model.

    :param request: HTTP request object.
    :type request: HttpRequest

    :param features: A queryset of features to update.
    :type features: QuerySet

    :return: An empty HTTP 200 response.
    :rtype: HttpResponse
    :raises: Http404
    """
    try:
        sequence_order_request = json.loads(request.body)
    except ValueError:
        raise Http404('Error JSON values')

    # Add dummy shift in the DB to avoid Integrity about unique_together
    for feature in features:
        feature.sequence_number += len(sequence_order_request)
        feature.save()

    for order_request in sequence_order_request:
        feature = features.get(id=order_request['id'])
        if feature:
            feature.sequence_number = order_request['sort_number']
            feature.save()

    return HttpResponse('')


class GetInvalidFurtherReadingLink(object):
    def __init__(self, project):
        self.project = project

    def get_all_invalid_url(self):
        from lesson.models.worksheet import Worksheet
        worksheets = Worksheet.objects.all().filter(
            section__project=self.project,
            furtherreading__isnull=False
        )
        result = []
        for worksheet in worksheets:
            worksheet_url = self.get_worksheet_url(
                worksheet_pk=worksheet.id,
                section_slug=worksheet.section.slug,
                project_slug=worksheet.section.project.slug
            )
            further_reading = worksheet.furtherreading_set.all()
            for obj in further_reading:
                urls = self.get_url_list(obj.text)
                for url in urls:
                    invalid_url = self.check_if_url_invalid(url)
                    if invalid_url:
                        result.append(
                            f'<a href="{worksheet_url}">{worksheet}</a> '
                            f'has invalid links or unavailable links: '
                            f'{url}'
                        )
        return result

    def get_url_list(self, text):
        # https://www.geeksforgeeks.org/python-check-url-string/
        regex = (
            r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"
            r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"
            r"(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)"
            r"|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
        url = re.findall(regex, text)
        return [x[0] for x in url]

    def check_if_url_invalid(self, url):
        """Return invalid url"""

        try:
            parsed_url = urlparse(url)  # e.g https://plugins.qgis.org/
            if not (all([parsed_url.scheme,  # e.g http
                         parsed_url.netloc])):  # e.g www.qgis.org
                return url
        except Exception:
            return url

        # Check if url is exist
        try:
            req = requests.head(url)
        except requests.exceptions.SSLError:
            req = requests.head(url, verify=False)
        except Exception:
            return url
        if req.status_code >= 400:
            return url
        return None

    def get_worksheet_url(self, worksheet_pk, section_slug, project_slug):
        return reverse('worksheet-detail', kwargs={
            'pk': worksheet_pk,
            'section_slug': section_slug,
            'project_slug': project_slug
        })
