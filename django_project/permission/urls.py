# coding=utf-8
"""Urls for changelog application."""
from django.conf.urls import patterns
from django.conf import settings

urlpatterns = patterns(
    '',
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
