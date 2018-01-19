# coding=utf-8
"""Urls for lesson application."""

from django.conf.urls import patterns, url

from django.conf import settings

from lesson.views.section import (
    SectionCreateView,
    SectionListView,
    SectionDeleteView,
    SectionUpdateView,
    SectionOrderView,
    SectionOrderSubmitView,
)
from lesson.views.worksheet import (
    WorksheetCreateView,
    WorksheetUpdateView,
    WorksheetDeleteView,
    WorksheetListView,
)
from lesson.views.specification import (
    SpecificationCreateView,
    SpecificationListView,
    SpecificationOrderView,
    SpecificationOrderSubmitView,
    SpecificationUpdateView,
    SpecificationDeleteView
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
    url(regex='^(?P<project_slug>[\w-]+)/section/order/$',
        view=SectionOrderView.as_view(),
        name='section-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/submit_order/$',
        view=SectionOrderSubmitView.as_view(),
        name='section-submit-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/(?P<slug>[\w-]+)/update/$',
        view=SectionUpdateView.as_view(),
        name='section-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/(?P<slug>[\w-]+)/delete/$',
        view=SectionDeleteView.as_view(),
        name='section-delete'),
    # Worksheet
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/create/$',
        view=WorksheetCreateView.as_view(),
        name='worksheet-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/update/(?P<pk>[\w-]+)/$',
        view=WorksheetUpdateView.as_view(),
        name='worksheet-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/delete/(?P<pk>[\w-]+)/$',
        view=WorksheetDeleteView.as_view(),
        name='worksheet-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/list/$',
        view=WorksheetListView.as_view(),
        name='worksheet-list'),
    # Specification
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/create/$',
        view=SpecificationCreateView.as_view(),
        name='specification-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/list/$',
        view=SpecificationListView.as_view(),
        name='specification-list'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/order/$',
        view=SpecificationOrderView.as_view(),
        name='specification-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/submit_order/$',
        view=SpecificationOrderSubmitView.as_view(),
        name='specification-submit-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/update/(?P<pk>[\w-]+)/$',
        view=SpecificationUpdateView.as_view(),
        name='specification-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/delete/(?P<pk>[\w-]+)/$',
        view=SpecificationDeleteView.as_view(),
        name='specification-delete'),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
