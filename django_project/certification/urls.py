# coding=utf-8
"""Urls for certification apps."""

from django.conf.urls import patterns, url
from views import (
    # Certifying Organisation.
    CertifyingOrganisationCreateView,
    CertifyingOrganisationDeleteView,
    CertifyingOrganisationDetailView,
    CertifyingOrganisationListView,
    CertifyingOrganisationUpdateView,
    PendingCertifyingOrganisationListView,
    ApproveCertifyingOrganisationView,

    # Course Type.
    CourseTypeCreateView,
    CourseTypeDeleteView,
    CourseTypeUpdateView,
    CourseTypeDetailView,

    # Course Convener.
    CourseConvenerCreateView,
    CourseConvenerDeleteView,
    CourseConvenerUpdateView,

    # Course.
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    CourseDetailView,

    # Training Center.
    TrainingCenterCreateView,
    TrainingCenterDetailView,
    TrainingCenterDeleteView,
    TrainingCenterUpdateView,

    # Attendee.
    AttendeeCreateView,

    # Course Attendee.
    CourseAttendeeCreateView,
    CourseAttendeeDeleteView,

    # Certificate.
    CertificateCreateView,
    CertificateDetailView,
    certificate_pdf_view,
    download_certificates_zip,
    update_paid_status,
    top_up_unavailable,
    email_all_attendees,
    regenerate_certificate,
    regenerate_all_certificate,

    # Validate Certificate.
    ValidateCertificate,

    # About.
    AboutView,
)


urlpatterns = patterns(
    '',

    # About page
    url(regex='^(?P<project_slug>[\w-]+)/about/$',
        view=AboutView.as_view(),
        name='about'),

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

    # Course Type.
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/create-coursetype/$',
        view=CourseTypeCreateView.as_view(),
        name='coursetype-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/coursetype/'
              '(?P<slug>[\w-]+)/update/$',
        view=CourseTypeUpdateView.as_view(),
        name='coursetype-update'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/coursetype/'
              '(?P<slug>[\w-]+)/delete/$',
        view=CourseTypeDeleteView.as_view(),
        name='coursetype-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/coursetype/(?P<slug>[\w-]+)/$',
        view=CourseTypeDetailView.as_view(),
        name='coursetype-detail'),

    # Course convener.
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/create-courseconvener/',
        view=CourseConvenerCreateView.as_view(),
        name='courseconvener-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/convener/'
              '(?P<slug>[\w-]+)/delete/$',
        view=CourseConvenerDeleteView.as_view(),
        name='courseconvener-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/convener/'
              '(?P<slug>[\w-]+)/update/$',
        view=CourseConvenerUpdateView.as_view(),
        name='courseconvener-update'),

    # Training Center management
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/create-trainingcenter/$',
        view=TrainingCenterCreateView.as_view(),
        name='trainingcenter-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/trainingcenter/'
              '(?P<slug>[\w-]+)/$',
        view=TrainingCenterDetailView.as_view(),
        name='trainingcenter-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/trainingcenter/'
              '(?P<slug>[\w-]+)/delete/$',
        view=TrainingCenterDeleteView.as_view(),
        name='trainingcenter-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/trainingcenter/'
              '(?P<slug>[\w-]+)/update/$',
        view=TrainingCenterUpdateView.as_view(),
        name='trainingcenter-update'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<slug>[\w-]+)/$',
        view=CourseDetailView.as_view(),
        name='course-detail'),

    # Attendee.
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<slug>[\w-]+)/create-attendee/$',
        view=AttendeeCreateView.as_view(),
        name='attendee-create'),

    # Course Attendee.
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<slug>[\w-]+)/create-courseattendee/$',
        view=CourseAttendeeCreateView.as_view(),
        name='courseattendee-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<course_slug>[\w-]+)/courseattendee/'
              '(?P<pk>[\w-]+)/delete/$',
        view=CourseAttendeeDeleteView.as_view(),
        name='courseattendee-delete'),

    # Certificate.
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<course_slug>[\w-]+)/courseattendee/'
              '(?P<pk>[\w-]+)/create-certificate/$',
        view=CertificateCreateView.as_view(),
        name='certificate-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<course_slug>[\w-]+)/courseattendee/'
              '(?P<pk>[\w-]+)/update-certificate-status/$',
        view=update_paid_status,
        name='paid-certificate'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/top-up/$',
        view=top_up_unavailable,
        name='top-up'),
    url(regex='^(?P<project_slug>[\w-]+)/certificate/'
              '(?P<id>[\w-]+)/$',
        view=CertificateDetailView.as_view(),
        name='certificate-details'),
    url(r'^(?P<project_slug>[\w-]+)/certifyingorganisation/'
        '(?P<organisation_slug>[\w-]+)/course/'
        '(?P<course_slug>[\w-]+)/print/(?P<pk>[\w-]+)/$',
        certificate_pdf_view, name='print-certificate'),
    url(r'^(?P<project_slug>[\w-]+)/certifyingorganisation/'
        '(?P<organisation_slug>[\w-]+)/course/'
        '(?P<course_slug>[\w-]+)/download_zip/$',
        download_certificates_zip, name='download_zip_all'),
    url(r'^(?P<project_slug>[\w-]+)/certifyingorganisation/'
        '(?P<organisation_slug>[\w-]+)/course/'
        '(?P<course_slug>[\w-]+)/send_email/$',
        email_all_attendees, name='send_email'),
    url(r'^(?P<project_slug>[\w-]+)/certifyingorganisation/'
        '(?P<organisation_slug>[\w-]+)/course/'
        '(?P<course_slug>[\w-]+)/regenerate-certificate/(?P<pk>[\w-]+)/$',
        regenerate_certificate, name='regenerate-certificate'),
    url(r'^(?P<project_slug>[\w-]+)/certifyingorganisation/'
        '(?P<organisation_slug>[\w-]+)/course/'
        '(?P<course_slug>[\w-]+)/regenerate-all-certificate/$',
        regenerate_all_certificate, name='regenerate-all-certificate'),

    # Course.
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/create-course/',
        view=CourseCreateView.as_view(),
        name='course-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<slug>[\w-]+)/update/$',
        view=CourseUpdateView.as_view(),
        name='course-update'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<slug>[\w-]+)/delete/$',
        view=CourseDeleteView.as_view(),
        name='course-delete'),

    # Search.
    url(regex='^(?P<project_slug>[\w-]+)/certificate/$',
        view=ValidateCertificate.as_view(), name='validate-certificate'),
)
