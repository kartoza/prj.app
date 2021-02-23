# coding=utf-8
"""Tools for the lesson app."""

import json
import os
import zipfile
from unidecode import unidecode

from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

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


def validate_zipfile(file) -> bool:
    try:
        zip = zipfile.ZipFile(file)
    except:
        raise ValidationError(_("Could not unzip file."))
    for zname in zip.namelist():
        if zname.find('..') != -1 or zname.find(os.path.sep) == 0:
            raise ValidationError(
                _('For security reasons, zip file cannot contain path '
                  'informations')
            )
        for forbidden_dir in ['__MACOSX', '.git', '__pycache__']:
            if forbidden_dir in zname.split('/'):
                raise ValidationError(
                    _("For security reasons, zip file cannot contain "
                      "'%s' directory" % (forbidden_dir,))
                )
    return True
