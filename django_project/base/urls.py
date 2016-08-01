# coding=utf-8
"""Urls for changelog application."""
from django.conf.urls import patterns, url
from django.conf import settings

from views import (
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
    custom_404
)

urlpatterns = patterns(
    '',
    # basic app views
    url(regex='^$',
        view=ProjectListView.as_view(),
        name='home'),

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
)

# Prevent cloudflare from showing an ad laden 404 with no context
handler404 = custom_404

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
