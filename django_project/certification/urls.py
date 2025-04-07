# coding=utf-8
"""Urls for certification apps."""

from django.conf.urls import url

from .api_views.checklist import UpdateChecklistReviewer
from .views import (
    # Certifying Organisation.
    CertifyingOrganisationCreateView,
    CertifyingOrganisationDeleteView,
    CertifyingOrganisationDetailView,
    CertifyingOrganisationListView,
    CertifyingOrganisationUpdateView,
    PendingCertifyingOrganisationListView,
    CertifyingOrganisationJson,
    ApproveCertifyingOrganisationView,
    reject_certifying_organisation,

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

    # Certificate type and checklist
    CertificationManagementView,
    update_project_certificate_view,
    ActivateChecklist,
    ArchiveChecklist,
    UpdateChecklistOrder,
    CertificateChecklistCreateView,

    # Training Center.
    TrainingCenterCreateView,
    TrainingCenterDetailView,
    TrainingCenterDeleteView,
    TrainingCenterUpdateView,

    # Attendee.
    AttendeeCreateView,
    CsvUploadView,
    AttendeeUpdateView,

    # Course Attendee.
    CourseAttendeeCreateView,
    CourseAttendeeDeleteView,

    # Certificate.
    CertificateCreateView,
    CertificateDetailView,
    certificate_pdf_view,
    download_certificates_zip,
    update_paid_status,
    email_all_attendees,
    regenerate_certificate,
    regenerate_all_certificate,
    generate_all_certificate,
    preview_certificate,
    CertificateRevokeView,
    GetCertificateTypeList,

    # Certificate for certifying organisation.
    OrganisationCertificateCreateView,
    organisation_certificate_pdf_view,
    OrganisationCertificateDetailView,

    # Validate Certificate.
    ValidateCertificate,
    ValidateCertificateOrganisation,

    # About.
    AboutView,
    TopUpView,

    CheckoutSessionSuccessView,
    CreateCheckoutSessionView
)
from .api_views.course import (
    GetUpcomingCourseProject,
    GetUpcomingCourseOrganisation,
    GetPastCourseProject,
    GetPastCourseOrganisation
)
from .api_views.get_status import GetStatus
from .api_views.update_status import UpdateStatusOrganisation
from .api_views.training_center import (
    GetTrainingCenterProjectLocation,
    GetTrainingCenterOrganisationLocation
)
from .api_views.invite_reviewer import InviteReviewerApiView
from .api_views.external_reviewer import UpdateExternalReviewerText


urlpatterns = [
    # About page
    url(regex='^(?P<project_slug>[\w-]+)/about/$',
        view=AboutView.as_view(),
        name='about'),

    # Certifying Organisation management
    url(regex='^(?P<project_slug>[\w-]+)/pending-certifyingorganisation/'
              'list/$',
        view=PendingCertifyingOrganisationListView.as_view(),
        name='pending-certifyingorganisation-list'),
    url(regex='^(?P<project_slug>[\w-]+)/'
              'certifyingorganisation-json/$',
        view=CertifyingOrganisationJson.as_view(),
        name='certifyingorganisation-list-json'),
    url(regex='^(?P<project_slug>[\w-]+)/approve-certifyingorganisation/'
              '(?P<slug>[\w-]+)/$',
        view=ApproveCertifyingOrganisationView.as_view(),
        name='certifyingorganisation-approve'),
    url(regex='^(?P<project_slug>[\w-]+)/reject-certifyingorganisation/'
              '(?P<slug>[\w-]+)/$',
        view=reject_certifying_organisation,
        name='certifyingorganisation-reject'),
    url(regex='^(?P<project_slug>[\w-]+)/update-status-certifyingorganisation/'
              '(?P<slug>[\w-]+)/$',
        view=UpdateStatusOrganisation.as_view(),
        name='certifyingorganisation-update-status'),
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
              '(?P<pk>[0-9]+)/update/$',
        view=CourseTypeUpdateView.as_view(),
        name='coursetype-update'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/coursetype/'
              '(?P<pk>[0-9]+)/delete/$',
        view=CourseTypeDeleteView.as_view(),
        name='coursetype-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/coursetype/(?P<pk>[0-9]+)/$',
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

    # Attendee.
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<slug>[\w-]+)/create-attendee/$',
        view=AttendeeCreateView.as_view(),
        name='attendee-create'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<course_slug>[\w-]+)/attendee/(?P<pk>[\w-]+)/update/$',
        view=AttendeeUpdateView.as_view(),
        name='attendee-update'),

    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<slug>[\w-]+)/upload/$',
        view=CsvUploadView.as_view(),
        name='upload-attendee'),

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

    # Certificate for certifying organisation
    url(regex='^(?P<project_slug>[\w-]+)/organisationcertificate/'
              '(?P<organisation_slug>[\w-]+)/issue/$',
        view=OrganisationCertificateCreateView.as_view(),
        name='issue-certificate-organisation'),
    url(regex='^(?P<project_slug>[\w-]+)/organisationcertificate/'
              '(?P<organisation_slug>[\w-]+)/print/$',
        view=organisation_certificate_pdf_view,
        name='print-certificate-organisation'),
    url(regex='^(?P<project_slug>[\w-]+)/organisationcertificate/'
              '(?P<id>[\w-]+)/$',
        view=OrganisationCertificateDetailView.as_view(),
        name='detail-certificate-organisation'),

    # Certificate Type and Checklist.
    url(regex='^(?P<project_slug>[\w-]+)/certification-management/$',
        view=CertificationManagementView.as_view(),
        name='certification-management-view'),
    url(regex='^(?P<project_slug>[\w-]+)/activate-checklist/$',
        view=ActivateChecklist.as_view(),
        name='activate-checklist'),
    url(regex='^(?P<project_slug>[\w-]+)/archive-checklist/$',
        view=ArchiveChecklist.as_view(),
        name='archive-checklist'),
    url(regex='^(?P<project_slug>[\w-]+)/update-checklist-order/$',
        view=UpdateChecklistOrder.as_view(),
        name='update-checklist-order'),
    url(regex='^(?P<project_slug>[\w-]+)/certificate-types-list/$',
        view=GetCertificateTypeList.as_view(),
        name='certificate-types-list'),
    url(regex='^(?P<project_slug>[\w-]+)/certificate-types/update/$',
        view=update_project_certificate_view,
        name='certificate-type-update'),
    url(regex='^(?P<project_slug>[\w-]+)/certificate-checklist/create/',
        view=CertificateChecklistCreateView.as_view(),
        name='certificate-checklist-create'),
    url(regex='^(?P<project_slug>[\w-]+)/update-checklist-reviewer/'
              '(?P<slug>[\w-]+)/',
        view=UpdateChecklistReviewer.as_view(),
        name='update-checklist-reviewer'),
    url(regex='^(?P<project_slug>[\w-]+)/invite-external-reviewer/'
              '(?P<slug>[\w-]+)/',
        view=InviteReviewerApiView.as_view(),
        name='invite-external-reviewer'),
    url(regex='^(?P<project_slug>[\w-]+)/update-external-reviewer-text/',
        view=UpdateExternalReviewerText.as_view(),
        name='update-external-reviewer-text'),

    # Certificate.
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<course_slug>[\w-]+)/courseattendee/'
              '(?P<pk>[\w-]+)/create-certificate/'
              '(?P<certificate_type_pk>[\w-]+)/$',
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
        view=TopUpView.as_view(),
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
        '(?P<course_slug>[\w-]+)/revoke/(?P<pk>[\w-]+)/$',
        CertificateRevokeView.as_view(), name='revoke-certificate'),
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
    url(r'^(?P<project_slug>[\w-]+)/certifyingorganisation/'
        '(?P<organisation_slug>[\w-]+)/course/'
        '(?P<course_slug>[\w-]+)/generate-all-certificate/$',
        generate_all_certificate, name='generate-all-certificate'),
    url(r'^(?P<project_slug>[\w-]+)/certifyingorganisation/'
        '(?P<organisation_slug>[\w-]+)/preview-certificate/$',
        preview_certificate, name='preview-certificate'),

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
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/course/'
              '(?P<slug>[\w-]+)/$',
        view=CourseDetailView.as_view(),
        name='course-detail'),

    # Search.
    url(regex='^(?P<project_slug>[\w-]+)/organisationcertificate/$',
        view=ValidateCertificateOrganisation.as_view(),
        name='validate-certificate-organisation'),
    url(regex='^(?P<project_slug>[\w-]+)/certificate/$',
        view=ValidateCertificate.as_view(), name='validate-certificate'),

    # API Views
    url(regex='^(?P<project_slug>[\w-]+)/get-status-list/$',
        view=GetStatus.as_view(), name='get-status-list'),

    # Feeds
    url(regex='^(?P<project_slug>[\w-]+)/feed/upcoming-course/$',
        view=GetUpcomingCourseProject.as_view(),
        name='feed-upcoming-project-course'),
    url(regex='^(?P<project_slug>[\w-]+)/feed/past-course/$',
        view=GetPastCourseProject.as_view(),
        name='feed-past-project-course'),
    url(regex='^(?P<project_slug>[\w-]+)/feed/training-center/$',
        view=GetTrainingCenterProjectLocation.as_view(),
        name='feed-training-center-project'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/feed/training-center/$',
        view=GetTrainingCenterOrganisationLocation.as_view(),
        name='feed-training-center'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/feed/upcoming-course/$',
        view=GetUpcomingCourseOrganisation.as_view(),
        name='feed-upcoming-course'),
    url(regex='^(?P<project_slug>[\w-]+)/certifyingorganisation/'
              '(?P<organisation_slug>[\w-]+)/feed/past-course/$',
        view=GetPastCourseOrganisation.as_view(),
        name='feed-past-course'),

    # Checkout
    url(
        '^checkout/$',
        CreateCheckoutSessionView.as_view(),
        name="checkout",
    ),
    url("^checkout-success/$",
        CheckoutSessionSuccessView.as_view(),
        name="checkout-success"),
]
