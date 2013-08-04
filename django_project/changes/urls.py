from django.conf.urls import patterns, url
from views import (
    HomeView,
    EntryDetailView,
    EntryDeleteView,
    EntryCreateView,
    EntryRenderListView,
    EntryListView,
    EntryUpdateView)
from django.conf import settings

urlpatterns = patterns(
    '',
    # basic app views
    url(regex='^$',
        view=HomeView.as_view(),
        name='home'),
    url(regex='^entry/render-list/$',
        view=EntryRenderListView.as_view(),
        name='entry-render-list'),
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
        name='entry-update')
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

