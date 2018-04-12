# coding=utf-8
"""View definitions."""

import pytz
from datetime import datetime

from django.contrib.gis.geos import Point
from django.shortcuts import render
from django.http import JsonResponse

from geocontext.utilities import convert_coordinate
from geocontext.models.context_service_registry import ContextServiceRegistry
from geocontext.models.context_cache import ContextCache
from geocontext.forms import GeoContextForm


def retrieve_context(x, y, service_registry_name, srid=4326):
    """Retrieve context from point x, y.

    :param x: X coordinate
    :type x: float

    :param y: Y Coordinate
    :type y: float

    :param service_registry_name: The name of service registry.
    :type service_registry_name: basestring

    :param srid: Spatial Reference ID
    :type srid: int

    :returns: Geometry of the context and the value.
    :rtype: (GEOSGeometry, basestring)
    """
    if srid != 4326:
        point = Point(*convert_coordinate(x, y, srid, 4326), srid=4326)
    else:
        point = Point(x, y, srid=4326)

    # Check in cache
    service_registry = ContextServiceRegistry.objects.get(
        name=service_registry_name)
    if not service_registry:
        raise Exception(
            'Service Registry is not Found for %s' % service_registry_name)
    caches = ContextCache.objects.filter(
        service_registry=service_registry)

    for cache in caches:
        if cache.geometry.contains(point):
            if datetime.utcnow().replace(tzinfo=pytz.UTC) < cache.expired_time:
                return cache.geometry, cache.value
            else:
                # No need to check the rest cache, since it always only 1
                # cache that intersect for a point.
                cache.delete()
                break

    # Can not find in caches, request from context service.
    return service_registry.retrieve_context_value(x, y, srid)


def get_context(request):
    """Get context view."""
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GeoContextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cleaned_data = form.cleaned_data
            x = cleaned_data['x']
            y = cleaned_data['y']
            srid = cleaned_data.get('srid', 4326)
            service_registry_name = cleaned_data['service_registry_name']
            geometry, value = retrieve_context(
                x, y, service_registry_name, srid)
            return JsonResponse({'value': value})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GeoContextForm(initial={'srid': 4326})

    return render(request, 'geocontext/get_context.html', {'form': form})
