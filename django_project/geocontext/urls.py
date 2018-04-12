# coding=utf-8
"""URLs for GeoContext app."""

from django.conf.urls import url
from geocontext.views import get_context

urlpatterns = [
    url(regex=r'^geocontext/$',
        view=get_context,
        name='geocontext-retrieve'),
]
