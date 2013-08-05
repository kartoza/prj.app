from django.conf.urls import patterns, url
from django.conf import settings

from views import (
    ProjectDetailView,
    ProjectDeleteView,
    ProjectCreateView,
    ProjectListView,
    ProjectUpdateView,
    CategoryDetailView,
    CategoryDeleteView,
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    VersionDetailView,
    VersionDeleteView,
    VersionCreateView,
    VersionListView,
    VersionUpdateView,
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

    # Category management
    url(regex='^Category/list/$',
        view=CategoryListView.as_view(),
        name='category-list'),
    url(regex='^Category/(?P<pk>\d+)/$',
        view=CategoryDetailView.as_view(),
        name='category-detail'),
    url(regex='^Category/delete/(?P<pk>\d+)/$',
        view=CategoryDeleteView.as_view(),
        name='category-delete'),
    url(regex='^Category/create/$',
        view=CategoryCreateView.as_view(),
        name='category-create'),
    url(regex='^Category/update/(?P<pk>\d+)/$',
        view=CategoryUpdateView.as_view(),
        name='category-update'),

    # Version management
    url(regex='^Version/list/$',
        view=VersionListView.as_view(),
        name='version-list'),
    url(regex='^Version/(?P<pk>\d+)/$',
        view=VersionDetailView.as_view(),
        name='version-detail'),
    url(regex='^Version/delete/(?P<pk>\d+)/$',
        view=VersionDeleteView.as_view(),
        name='version-delete'),
    url(regex='^Version/create/$',
        view=VersionCreateView.as_view(),
        name='version-create'),
    url(regex='^Version/update/(?P<pk>\d+)/$',
        view=VersionUpdateView.as_view(),
        name='version-update'),

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

