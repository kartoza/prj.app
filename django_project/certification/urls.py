# coding=utf-8
"""urls for certification application"""

from django.conf.urls import patterns, url
from views import (
    # Certifying Organisation
    CertifyingOrganisationCreateView,
    CertifyingOrganisationDeleteView,
    CertifyingOrganisationDetailView,
    CertifyingOrganisationListView,
    CertifyingOrganisationUpdateView,
    PendingCertifyingOrganisationListView,
    ApproveCertifyingOrganisationView,

    CourseTypeCreateView,
    CourseTypeDeleteView,
    CourseTypeUpdateView,
)


urlpatterns = patterns(
    '',

    # Certifying Organisation management
    url(regex='^(?P<project_slug>[\w-]+)/pending-certifyingorganisation/'
              'list/$',
        view=PendingCertifyingOrganisationListView.as_view(),
        name='pending-certifyingorganisation-list'),
    url(regex='^(?P<project_slug>[\w-]+)/approve-certifyingorganisation/'
              '(?P<slug>[\w-]+)/$',
        view=ApproveCertifyingOrganisationView.as_view(),
        name='certifyingorganisation-approve'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/list/$',
        view=CertifyingOrganisationListView.as_view(),
        name='certifyingorganisation-list'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<slug>[\w-]+)/$',
        view=CertifyingOrganisationDetailView.as_view(),
        name='certifyingorganisation-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<slug>[\w-]+)/delete/$',
        view=CertifyingOrganisationDeleteView.as_view(),
        name='certifyingorganisation-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-certifyingorganisation/$',
        view=CertifyingOrganisationCreateView.as_view(),
        name='certifyingorganisation-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<slug>[\w-]+)/update/$',
        view=CertifyingOrganisationUpdateView.as_view(),
        name='certifyingorganisation-update'),

    # Course Type
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/create-coursetype/$',
        view=CourseTypeCreateView.as_view(),
        name='coursetype-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/(?P<slug>[\w-]+)/update/$',
        view=CourseTypeUpdateView.as_view(),
        name='coursetype-update'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/(?P<slug>[\w-]+)/delete/$',
        view=CourseTypeDeleteView.as_view(),
        name='coursetype-delete'),
)
