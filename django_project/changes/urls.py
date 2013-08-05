from django.conf.urls import patterns, url
from django.conf import settings

from views import (
    ProjectDetailView,
    ProjectDeleteView,
    ProjectCreateView,
    ProjectListView,
    ProjectUpdateView,
    EntryDetailView,
    EntryDeleteView,
    EntryCreateView,
    EntryListView,
    EntryUpdateView)

urlpatterns = patterns(
    '',
    # basic app views
    url(regex='^$',
        view=ProjectListView.as_view(),
        name='home'),
    # Project management
    url(regex='^project/list/$',
        view=ProjectListView.as_view(),
        name='project-list'),
    url(regex='^project/(?P<pk>\d+)/$',
        view=ProjectDetailView.as_view(),
        name='project-detail'),
    url(regex='^project/delete/(?P<pk>\d+)/$',
        view=ProjectDeleteView.as_view(),
        name='project-delete'),
    url(regex='^project/create/$',
        view=ProjectCreateView.as_view(),
        name='project-create'),
    url(regex='^project/update/(?P<pk>\d+)/$',
        view=ProjectUpdateView.as_view(),
        name='project-update'),

    # Changelog entry management
    url(regex='^entry/list/$',
        view=EntryListView.as_view(),
        name='entry-list'),
    url(regex='^entry/(?P<pk>\d+)/$',
        view=EntryDetailView.as_view(),
        name='entry-detail'),
    url(regex='^entry/delete/(?P<pk>\d+)/$',
        view=EntryDeleteView.as_view(),
        name='entry-delete'),
    url(regex='^entry/create/$',
        view=EntryCreateView.as_view(),
        name='entry-create'),
    url(regex='^entry/update/(?P<pk>\d+)/$',
        view=EntryUpdateView.as_view(),
        name='entry-update'),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

