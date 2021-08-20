# coding=utf-8
"""Tools for the lesson app."""

import json
import os
import zipfile
import re

from unidecode import unidecode

from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from core.settings.contrib import STOP_WORDS


ZIP_IGNORE_FILE = os.path.join(
    os.path.dirname(__file__), 'zip_ignore_files.txt')


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


def validate_zipfile(file) -> bool:
    """Validate the zipfile upon upload in a worksheet."""

    try:
        zip = zipfile.ZipFile(file)
    except Exception:
        raise ValidationError(_("Could not unzip file."))

    ignore_list = get_ignore_file_list(ZIP_IGNORE_FILE)
    for zname in zip.namelist():
        if zname.find('..') != -1 or zname.find(os.path.sep) == 0:
            raise ValidationError(
                _('For security reasons, zip file cannot contain path '
                  'informations')
            )
        for forbidden_dir in ignore_list:
            if forbidden_dir in zname.split('/'):
                raise ValidationError(
                    _("For security reasons, zip file cannot contain "
                      "'%s' directory" % (forbidden_dir,))
                )
    return True


def get_ignore_file_list(ignore_file) -> list:
    """Read the zip_ignore_files.txt and put the content into a list."""
    try:
        result = []
        with open(ignore_file) as f:
            files = f.readlines()
            for file in files:
                ignore = file.strip()
                if ignore:
                    result.append(ignore)
        return result
    except FileNotFoundError:
        return []


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
