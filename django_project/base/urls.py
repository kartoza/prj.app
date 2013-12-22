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
    ApproveProjectView)

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
    url(regex='^project/(?P<slug>[\w-]+)/delete/$',
        view=ProjectDeleteView.as_view(),
        name='project-delete'),
    url(regex='^project/create/$',
        view=ProjectCreateView.as_view(),
        name='project-create'),
    url(regex='^project/(?P<slug>[\w-]+)/update/$',
        view=ProjectUpdateView.as_view(),
        name='project-update'),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
