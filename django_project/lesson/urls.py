# coding=utf-8
"""Urls for lesson application."""

from django.conf.urls import patterns, url

from django.conf import settings

from lesson.views.section import (
    SectionCreateView,
    SectionListView,
    SectionDetailView,
    SectionDeleteView,
    SectionUpdateView,
)

urlpatterns = patterns(
    '',
    # Section
    url(regex='^(?P<project_slug>[\w-]+)/section/create/$',
        view=SectionCreateView.as_view(),
        name='section-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/list/$',
        view=SectionListView.as_view(),
        name='section-list'),
    url(regex='^(?P<project_slug>[\w-]+)/section/(?P<slug>[\w-]+)/$',
        view=SectionDetailView.as_view(),
        name='section-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/section/(?P<slug>[\w-]+)/delete/$',
        view=SectionDeleteView.as_view(),
        name='section-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<slug>[\w-]+)/update/$',
        view=SectionUpdateView.as_view(),
        name='section-update'),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
