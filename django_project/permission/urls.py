# coding=utf-8
"""Urls for changelog application."""
from django.conf.urls import patterns, url
from permission.views.user_manager import UserManagerListView
from permission.views.administrator import (
    ProjectAdministratorCreateView,
    ProjectAdministratorDeleteView
)
from permission.views.collaborator import (
    ProjectCollaboratorCreateView,
    ProjectCollaboratorDeleteView
)

urlpatterns = patterns(
    '',
    url(regex='^(?P<username>[\w\-]+)/user-manager/$',
        view=UserManagerListView.as_view(),
        name='user-manager'),
    url(regex='^(?P<project_slug>[\w-]+)/administrator/create/$',
        view=ProjectAdministratorCreateView.as_view(),
        name='administrator-create'),
    url(regex='^(?P<project_slug>[\w-]+)/collaborator/create/$',
        view=ProjectCollaboratorCreateView.as_view(),
        name='collaborator-create'),
    url(regex='^administrator/(?P<pk>\d+)/delete/$',
        view=ProjectAdministratorDeleteView.as_view(),
        name='administrator-delete'),
    url(regex='^collaborator/(?P<pk>\d+)/delete/$',
        view=ProjectCollaboratorDeleteView.as_view(),
        name='collaborator-delete'),
)
