# coding=utf-8
"""Tools for the lesson app."""

import json
import re

from unidecode import unidecode

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


class GetAllFurtherReadingLink(object):
    def __init__(self, project):
        self.project = project

    def get_all_url(self):
        from lesson.models.worksheet import Worksheet
        worksheets = Worksheet.objects.all().filter(
            section__project=self.project,
            furtherreading__isnull=False
        ).distinct()
        result = []
        for worksheet in worksheets:
            worksheet_url = self.get_worksheet_url(
                worksheet_pk=worksheet.id,
                section_slug=worksheet.section.slug,
                project_slug=worksheet.section.project.slug
            )
            further_reading = worksheet.furtherreading_set.all().distinct()
            for obj in further_reading:
                urls = self.get_url_list(obj.text)
                for url in urls:
                    ctx = {
                        'worksheet_url': worksheet_url,
                        'worksheet': worksheet.module,
                        'further_reading_url': url
                    }
                    result.append(ctx)
        return result

    def get_url_list(self, text):
        urls = re.findall(r'href=[\'"]?\s*([^\'">]+)', text)
        result = [url.strip() for url in urls]
        return result

    def get_worksheet_url(self, worksheet_pk, section_slug, project_slug):
        return reverse('worksheet-detail', kwargs={
            'pk': worksheet_pk,
            'section_slug': section_slug,
            'project_slug': project_slug
        })
