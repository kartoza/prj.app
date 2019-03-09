# coding=utf-8
# flake8: noqa
"""Urls for changelog application."""

from django.conf.urls import patterns, url, include  # noqa

from django.conf import settings

from feeds.version import RssVersionFeed, AtomVersionFeed
from feeds.entry import RssEntryFeed, AtomEntryFeed
from feeds.sponsor import (
    RssSponsorFeed,
    RssPastSponsorFeed,
    AtomSponsorFeed,
    AtomPastSponsorFeed,
    JSONSponsorFeed,
    JSONPastSponsorFeed
)
from views import (
    # Category
    CategoryDetailView,
    CategoryDeleteView,
    CategoryCreateView,
    CategoryListView,
    CategoryOrderView,
    CategoryOrderSubmitView,
    JSONCategoryListView,
    CategoryUpdateView,
    # Version
    VersionMarkdownView,
    VersionDetailView,
    VersionThumbnailView,
    VersionDeleteView,
    VersionCreateView,
    VersionListView,
    VersionUpdateView,
    VersionDownload,
    VersionDownloadGnu,
    VersionSponsorDownload,
    # Entry
    EntryDetailView,
    EntryDeleteView,
    EntryCreateView,
    EntryUpdateView,
    EntryOrderView,
    EntryOrderSubmitView,

    # Sponsor
    SponsorDetailView,
    SponsorDeleteView,
    SponsorCreateView,
    SponsorListView,
    SponsorWorldMapView,
    JSONSponsorListView,
    SponsorUpdateView,
    PendingSponsorListView,
    ApproveSponsorView,
    GenerateSponsorPDFView,

    # Sponsorship Level

    SponsorshipLevelDetailView,
    SponsorshipLevelDeleteView,
    SponsorshipLevelCreateView,
    SponsorshipLevelListView,
    JSONSponsorshipLevelListView,
    SponsorshipLevelUpdateView,
    PendingSponsorshipLevelListView,
    ApproveSponsorshipLevelView,

    # Sponsorship Period

    SponsorshipPeriodDetailView,
    SponsorshipPeriodDeleteView,
    SponsorshipPeriodCreateView,
    SponsorshipPeriodListView,
    JSONSponsorshipPeriodListView,
    SponsorshipPeriodUpdateView,
    PendingSponsorshipPeriodListView,
    ApproveSponsorshipPeriodView,

    generate_sponsor_cloud,
)

urlpatterns = patterns(
    '',
    # Category management

    # This view is only accessible via ajax
    url(regex='^json-category/list/(?P<version>\d+)/$',
        view=JSONCategoryListView.as_view(),
        name='json-category-list'),
    url(regex='^(?P<project_slug>[\w-]+)/category/list/$',
        view=CategoryListView.as_view(),
        name='category-list'),
    url(regex='^(?P<project_slug>[\w-]+)/category/order/$',
        view=CategoryOrderView.as_view(),
        name='category-order'),
    url(regex='^(?P<project_slug>[\w-]+)/category/submit_order/$',
        view=CategoryOrderSubmitView.as_view(),
        name='category-submit-order'),
    url(regex='^(?P<project_slug>[\w-]+)/category/(?P<slug>[\w-]+)/$',
        view=CategoryDetailView.as_view(),
        name='category-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/category/(?P<slug>[\w-]+)/delete/$',
        view=CategoryDeleteView.as_view(),
        name='category-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-category/$',
        view=CategoryCreateView.as_view(),
        name='category-create'),
    url(regex='^(?P<project_slug>[\w-]+)/category/(?P<slug>[\w-]+)/update/$',
        view=CategoryUpdateView.as_view(),
        name='category-update'),

    # Version management
    url(regex='^(?P<project_slug>[\w-]+)/version/list/$',
        view=VersionListView.as_view(),
        name='version-list'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/markdown/$',
        view=VersionMarkdownView.as_view(),
        name='version-markdown'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/$',
        view=VersionDetailView.as_view(),
        name='version-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/thumbs/$',
        view=VersionThumbnailView.as_view(),
        name='version-thumbs'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/delete/$',
        view=VersionDeleteView.as_view(),
        name='version-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-version/$',
        view=VersionCreateView.as_view(),
        name='version-create'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/update/$',
        view=VersionUpdateView.as_view(),
        name='version-update'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/download/$',
        view=VersionDownload.as_view(),
        name='version-download'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/gnu/$',
        view=VersionDownloadGnu.as_view(),
        name='version-download-gnu'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/downloadsponsor/$',
        view=VersionSponsorDownload.as_view(),
        name='version-sponsor-download'),

    # Changelog entry management
    url(regex='^entry/(?P<pk>\d+)$',
        view=EntryDetailView.as_view(),
        name='entry-detail'),
    url(regex='^entry/delete/(?P<pk>\d+)$',
        view=EntryDeleteView.as_view(),
        name='entry-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/(?P<version_slug>[\w.-]+)/'
              'create-entry/$',
        view=EntryCreateView.as_view(),
        name='entry-create'),
    url(regex='^entry/update/(?P<pk>\d+)$',
        view=EntryUpdateView.as_view(),
        name='entry-update'),
    url(regex='^(?P<project_pk>[\w-]+)/version/(?P<version_pk>[\w.-]+)/'
              'order/(?P<category_pk>[\w-]+)$',
        view=EntryOrderView.as_view(),
        name='entry-order'),
    url(regex='^(?P<project_pk>[\w-]+)/version/(?P<version_pk>[\w.-]+)/'
              'submit-order/(?P<category_pk>[\w-]+)$',
        view=EntryOrderSubmitView.as_view(),
        name='entry-submit-order'),

    # Feeds
    url(regex='^(?P<project_slug>[\w-]+)/rss/latest-version/$',
        view=RssVersionFeed(),
        name='latest-version-rss-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/atom/latest-version/$',
        view=AtomVersionFeed(),
        name='latest-version-atom-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/rss/latest-entry/$',
        view=RssEntryFeed(),
        name='latest-entry-rss-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/atom/latest-entry/$',
        view=AtomEntryFeed(),
        name='latest-entry-atom-feed'),

    # Feeds specific version and projects
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<version_slug>['
              '\w.-]+)/rss$',
        view=RssEntryFeed(),
        name='entry-rss-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<version_slug>['
              '\w.-]+)/atom$',
        view=AtomEntryFeed(),
        name='entry-atom-feed'),

    url(regex='^(?P<project_slug>[\w-]+)/sponsor/(?P<slug>[\w-]+)/invoice/$',
        view=GenerateSponsorPDFView.as_view(),
        name='sponsor-invoice'),

    # Feeds sponsors in a specific project
    url(regex='^(?P<project_slug>[\w-]+)/sponsors/rss/$',
        view=RssSponsorFeed(),
        name='sponsor-rss-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/past-sponsors/rss/$',
        view=RssPastSponsorFeed(),
        name='past-sponsor-rss-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsors/atom/$',
        view=AtomSponsorFeed(),
        name='sponsor-atom-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/past-sponsors/atom/$',
        view=AtomPastSponsorFeed(),
        name='past-sponsor-atom-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsors/json/$',
        view=JSONSponsorFeed(),
        name='sponsor-json-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/past-sponsors/json/$',
        view=JSONPastSponsorFeed(),
        name='past-sponsor-json-feed'),

    # User map
    # url(r'^user-map/', include('user_map.urls')),

    # Sponsor management

    # This view is only accessible via ajax
    url(regex='^json-sponsor/list/(?P<version>\d+)/$',
        view=JSONSponsorListView.as_view(),
        name='json-sponsor-list'),
    url(regex='^(?P<project_slug>[\w-]+)/pending-sponsors/list/$',
        view=PendingSponsorListView.as_view(),
        name='pending-sponsor-list'),
    url(regex='^(?P<project_slug>[\w-]+)/approve-sponsor/(?P<slug>[\w-]+)/$',
        view=ApproveSponsorView.as_view(),
        name='sponsor-approve'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsors/list/$',
        view=SponsorListView.as_view(),
        name='sponsor-list'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsors/world-map/$',
        view=SponsorWorldMapView.as_view(),
        name='sponsor-world-map'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsor/(?P<slug>[\w-]+)/$',
        view=SponsorDetailView.as_view(),
        name='sponsor-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsor/(?P<slug>[\w-]+)/delete/$',
        view=SponsorDeleteView.as_view(),
        name='sponsor-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-sponsor/$',
        view=SponsorCreateView.as_view(),
        name='sponsor-create'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsor/(?P<slug>[\w-]+)/update/$',
        view=SponsorUpdateView.as_view(),
        name='sponsor-update'),

    # Sponsorship Level management

    # This view is only accessible via ajax
    url(regex='^json-sponsorshiplevel/list/(?P<version>\d+)/$',
        view=JSONSponsorshipLevelListView.as_view(),
        name='json-sponsorshiplevel-list'),
    url(regex='^(?P<project_slug>[\w-]+)/pending-sponsorshiplevel/list/$',
        view=PendingSponsorshipLevelListView.as_view(),
        name='pending-sponsorshiplevel-list'),
    url(regex='^(?P<project_slug>[\w-]+)/approve-sponsorshiplevel/(?P<slug>[\w-]+)/$',
        view=ApproveSponsorshipLevelView.as_view(),
        name='sponsorshiplevel-approve'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsorshiplevel/list/$',
        view=SponsorshipLevelListView.as_view(),
        name='sponsorshiplevel-list'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsorshiplevel/(?P<slug>[\w-]+)/$',
        view=SponsorshipLevelDetailView.as_view(),
        name='sponsorshiplevel-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsorshiplevel/(?P<slug>[\w-]+)/delete/$',
        view=SponsorshipLevelDeleteView.as_view(),
        name='sponsorshiplevel-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-sponsorshiplevel/$',
        view=SponsorshipLevelCreateView.as_view(),
        name='sponsorshiplevel-create'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsorshiplevel/(?P<slug>[\w-]+)/update/$',
        view=SponsorshipLevelUpdateView.as_view(),
        name='sponsorshiplevel-update'),

    # Sponsorship Period management

    # This view is only accessible via ajax
    url(regex='^json-sponsorshipperiod/list/(?P<version>\d+)/$',
        view=JSONSponsorshipPeriodListView.as_view(),
        name='json-sponsorshipperiod-list'),
    url(regex='^(?P<project_slug>[\w-]+)/pending-sponsorshipperiod/list/$',
        view=PendingSponsorshipPeriodListView.as_view(),
        name='pending-sponsorshipperiod-list'),
    url(regex='^(?P<project_slug>[\w-]+)/approve-sponsorshipperiod/(?P<slug>[\w-]+)/$',
        view=ApproveSponsorshipPeriodView.as_view(),
        name='sponsorshipperiod-approve'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsorshipperiod/list/$',
        view=SponsorshipPeriodListView.as_view(),
        name='sponsorshipperiod-list'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsorshipperiod/(?P<slug>[\w-]+)/$',
        view=SponsorshipPeriodDetailView.as_view(),
        name='sponsorshipperiod-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsorshipperiod/(?P<slug>[\w-]+)/delete/$',
        view=SponsorshipPeriodDeleteView.as_view(),
        name='sponsorshipperiod-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-sponsorshipperiod/$',
        view=SponsorshipPeriodCreateView.as_view(),
        name='sponsorshipperiod-create'),
    url(regex='^(?P<project_slug>[\w-]+)/sponsorshipperiod/(?P<slug>[\w-]+)/update/$',
        view=SponsorshipPeriodUpdateView.as_view(),
        name='sponsorshipperiod-update'),

    # Sponsor Cloud
    url(regex='^(?P<project_slug>[\w-]+)/sponsor-cloud/$',
        view=generate_sponsor_cloud,
        name='sponsor-cloud'),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
