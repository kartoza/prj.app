# coding=utf-8
"""Urls for changelog application."""
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

from .views import (
    # Project
    ProjectDetailView,
    ProjectDeleteView,
    ProjectCreateView,
    ProjectListView,
    ProjectUpdateView,
    PendingProjectListView,
    ApproveProjectView,
    ProjectBallotListView,
    GithubProjectView,
    GithubListView,
    GithubOrgsView,
    GithubSubmitView,
    custom_404,
    project_sponsor_programme,
    preview_certificate,

    DomainNotFound,
    RegisterDomainView,
    DomainThankYouView,
    DomainListView,
    PendingDomainListView,
    ApproveDomainView,
    DomainDeleteView,
    DomainUpdateView,

    CreateOrganisationView,
    OrganisationListView,
    ApproveOrganisationView,
    PendingOrganisationListView,
    OrganisationDeleteView,
    OrganisationUpdateView,

    UserDetailView,
    UserUpdateView,
    project_flatpage
)
from .api_views.stripe_intent import StripeIntent

urlpatterns = [
    # basic app views
    url(regex='^$',
        view=ProjectListView.as_view(),
        name='home'),

    url(regex='^profile/$',
        view=UserDetailView.as_view(),
        name='user-profile'),
    url(regex='^edit-profile/(?P<pk>[\w-]+)/$',
        view=UserUpdateView.as_view(),
        name='edit-profile'),

    # Custom domain management
    url(regex='^domain-not-found/$',
        view=DomainNotFound.as_view(),
        name='domain-not-found'),
    url(regex='^register-domain/$',
        view=RegisterDomainView.as_view(),
        name='register-domain'),
    url(regex='^domain-success/$',
        view=DomainThankYouView.as_view(),
        name='domain-registered'),
    url(regex='^domain-list/$',
        view=DomainListView.as_view(),
        name='domain-list'),
    url(regex='^pending-list-domain/$',
        view=PendingDomainListView.as_view(),
        name='domain-pending-list'),
    url(regex='^domain-approve/(?P<pk>[\w-]+)/$',
        view=ApproveDomainView.as_view(),
        name='domain-approve'),
    url(regex='^domain/(?P<pk>[\w-]+)/delete/$',
        view=DomainDeleteView.as_view(),
        name='domain-delete'),
    url(regex='^domain/(?P<pk>[\w-]+)/update/$',
        view=DomainUpdateView.as_view(),
        name='domain-update'),

    # Organisation management
    url(regex='^create-organisation/$',
        view=CreateOrganisationView.as_view(),
        name='create-organisation'),
    url(regex='^list-organisation/$',
        view=OrganisationListView.as_view(),
        name='list-organisation'),
    url(regex='^pending-list-organisation/$',
        view=PendingOrganisationListView.as_view(),
        name='pending-list-organisation'),
    url(regex='^approve-organisation/(?P<pk>[\w-]+)/$',
        view=ApproveOrganisationView.as_view(),
        name='approve-organisation'),
    url(regex='^organisation/(?P<pk>[\w-]+)/delete/$',
        view=OrganisationDeleteView.as_view(),
        name='organisation-delete'),
    url(regex='^organisation/(?P<pk>[\w-]+)/update/$',
        view=OrganisationUpdateView.as_view(),
        name='organisation-update'),

    # Project management
    url(regex='^pending-project/list/$',
        view=PendingProjectListView.as_view(),
        name='pending-project-list'),
    url(regex='^approve-project/(?P<slug>[\w-]+)/$',
        view=ApproveProjectView.as_view(),
        name='project-approve'),
    url(regex='^project/list/$',
        view=ProjectListView.as_view(),
        name='project-list'),
    url(regex='^project/preview-certificate/$',
        view=preview_certificate,
        name='preview-certificate-project'),
    url(regex='^(?P<slug>[\w-]+)/$',
        view=ProjectDetailView.as_view(),
        name='project-detail'),
    url(regex='^(?P<slug>[\w-]+)/ballots/$',
        view=ProjectBallotListView.as_view(),
        name='project-ballot-list'),
    url(regex='^project/(?P<slug>[\w-]+)/delete/$',
        view=ProjectDeleteView.as_view(),
        name='project-delete'),
    url(regex='^project/create/$',
        view=ProjectCreateView.as_view(),
        name='project-create'),
    url(regex='^project/(?P<slug>[\w-]+)/update/$',
        view=ProjectUpdateView.as_view(),
        name='project-update'),
    url(regex='^project/github-repo/$',
        view=GithubProjectView.as_view(),
        name='github-repo-view'),
    url(regex='^project/get-github-repo/$',
        view=GithubListView.as_view(),
        name='get-github-repo'),
    url(regex='^project/get-github-repo-org/(?P<org>[\w-]+)/$',
        view=GithubListView.as_view(),
        name='get-github-repo-org'),
    url(regex='^project/get-github-orgs/$',
        view=GithubOrgsView.as_view(),
        name='get-github-orgs'),
    url(regex='^project/submit-github-repo/$',
        view=GithubSubmitView.as_view(),
        name='submit-github-repo'),
    url(regex='^(?P<slug>[\w-]+)/sponsorship-programme/$',
        view=project_sponsor_programme,
        name='sponsor-programme'),
    url(regex='^stripe-intent/(?P<amount>[\d-]+)/$',
        view=StripeIntent.as_view(),
        name='stripe-intent'),

    # Project flatpage urls
    url(r'^(?P<project_slug>[\w-]+)/flatpage(?P<url>.*)$',
        project_flatpage,
        name='project_flatpage'),
]

# Prevent cloudflare from showing an ad laden 404 with no context
handler404 = custom_404

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT})]
