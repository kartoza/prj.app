# coding=utf-8
# flake8: noqa
"""Urls for changelog application."""

from django.conf.urls import url, include  # noqa
from django.views.static import serve

from django.conf import settings

from .feeds.version import RssVersionFeed, AtomVersionFeed
from .feeds.entry import RssEntryFeed, AtomEntryFeed
from .feeds.sponsor import (
    RssSponsorFeed,
    RssPastSponsorFeed,
    AtomSponsorFeed,
    AtomPastSponsorFeed,
    JSONSponsorFeed,
    JSONPastSponsorFeed
)
from changes.api_views.lock_version import LockVersion, UnlockVersion
from .views import (
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
    RejectedSustainingMemberList,
    ApproveSponsorView,
    RejectSponsorView,
    GenerateSponsorPDFView,
    FutureSponsorListView,
    SustainingMembership,
    SustainingMemberUpdateView,
    SustainingMemberPeriodCreateView,
    SustainingMemberPeriodUpdateView,

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
    FetchGithubPRs,
    FetchRepoLabels,
    FetchCategory,
    download_all_referenced_images,
)
from changes.views.sustaining_member import (
    SustainingMemberCreateView
)

urlpatterns = [
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
    url(regex='^(?P<project_pk>[\w-]+)/version/fetch-github-pr/$',
        view=FetchGithubPRs.as_view(),
        name='fetch-pr-github'),
    url(regex='^(?P<project_pk>[\w-]+)/version/fetch-github-label/$',
        view=FetchRepoLabels.as_view(),
        name='fetch-labels-github'),
    url(regex='^(?P<project_pk>[\w-]+)/version/fetch-category/$',
        view=FetchCategory.as_view(),
        name='fetch-category'),
    url(regex='^(?P<project_slug>[\w-]+)/version/list/$',
        view=VersionListView.as_view(),
        name='version-list'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/'
              'download-referenced-images/$',
        view=download_all_referenced_images,
        name='download-referenced-images'),
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
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/downloadmember/$',
        view=VersionSponsorDownload.as_view(),
        name='version-sponsor-download'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/locked/$',
        view=LockVersion.as_view(),
        name='version-locked'),
    url(regex='^(?P<project_slug>[\w-]+)/version/(?P<slug>[\w.-]+)/unlocked/$',
        view=UnlockVersion.as_view(),
        name='version-unlocked'),

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

    url(regex='^(?P<project_slug>[\w-]+)/member/(?P<slug>[\w-]+)/invoice/$',
        view=GenerateSponsorPDFView.as_view(),
        name='sponsor-invoice'),

    # Feeds sponsors in a specific project
    url(regex='^(?P<project_slug>[\w-]+)/members/rss/$',
        view=RssSponsorFeed(),
        name='sponsor-rss-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/past-members/rss/$',
        view=RssPastSponsorFeed(),
        name='past-sponsor-rss-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/members/atom/$',
        view=AtomSponsorFeed(),
        name='sponsor-atom-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/past-members/atom/$',
        view=AtomPastSponsorFeed(),
        name='past-sponsor-atom-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/members/json/$',
        view=JSONSponsorFeed(),
        name='sponsor-json-feed'),
    url(regex='^(?P<project_slug>[\w-]+)/past-members/json/$',
        view=JSONPastSponsorFeed(),
        name='past-sponsor-json-feed'),

    # User map
    # url(r'^user-map/', include('user_map.urls')),

    # Sponsor management

    # This view is only accessible via ajax
    url(regex='^json-member/list/(?P<version>\d+)/$',
        view=JSONSponsorListView.as_view(),
        name='json-sponsor-list'),
    url(regex='^(?P<project_slug>[\w-]+)/pending-members/list/$',
        view=PendingSponsorListView.as_view(),
        name='pending-sponsor-list'),
    url(regex='^(?P<project_slug>[\w-]+)/sustaining-members-rejected/list/$',
        view=RejectedSustainingMemberList.as_view(),
        name='sustaining-members-rejected-list'),
    url(regex='^(?P<project_slug>[\w-]+)/approve-member/(?P<slug>[\w-]+)/$',
        view=ApproveSponsorView.as_view(),
        name='sponsor-approve'),
    url(regex='^(?P<project_slug>[\w-]+)/reject-member/(?P<member_id>\d+)/$',
        view=RejectSponsorView.as_view(),
        name='sponsor-reject'),
    url(regex='^(?P<project_slug>[\w-]+)/members/list/$',
        view=SponsorListView.as_view(),
        name='sponsor-list'),
    url(regex='^(?P<project_slug>[\w-]+)/future-members/list/$',
        view=FutureSponsorListView.as_view(),
        name='future-sponsor-list'),
    url(regex='^(?P<project_slug>[\w-]+)/members/world-map/$',
        view=SponsorWorldMapView.as_view(),
        name='sponsor-world-map'),
    url(regex='^(?P<project_slug>[\w-]+)/member/(?P<slug>[\w-]+)/$',
        view=SponsorDetailView.as_view(),
        name='sponsor-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/member/(?P<slug>[\w-]+)/delete/$',
        view=SponsorDeleteView.as_view(),
        name='sponsor-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-member/$',
        view=SponsorCreateView.as_view(),
        name='sponsor-create'),
    url(regex='^(?P<project_slug>[\w-]+)/member/(?P<slug>[\w-]+)/update/$',
        view=SponsorUpdateView.as_view(),
        name='sponsor-update'),

    # Sponsorship Level management

    # This view is only accessible via ajax
    url(regex='^json-membershiplevel/list/(?P<version>\d+)/$',
        view=JSONSponsorshipLevelListView.as_view(),
        name='json-sponsorshiplevel-list'),
    url(regex='^(?P<project_slug>[\w-]+)/pending-membershiplevel/list/$',
        view=PendingSponsorshipLevelListView.as_view(),
        name='pending-sponsorshiplevel-list'),
    url(regex='^(?P<project_slug>[\w-]+)/approve-membershiplevel/(?P<slug>[\w-]+)/$',
        view=ApproveSponsorshipLevelView.as_view(),
        name='sponsorshiplevel-approve'),
    url(regex='^(?P<project_slug>[\w-]+)/membershiplevel/list/$',
        view=SponsorshipLevelListView.as_view(),
        name='sponsorshiplevel-list'),
    url(regex='^(?P<project_slug>[\w-]+)/membershiplevel/(?P<slug>[\w-]+)/$',
        view=SponsorshipLevelDetailView.as_view(),
        name='sponsorshiplevel-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/membershiplevel/(?P<slug>[\w-]+)/delete/$',
        view=SponsorshipLevelDeleteView.as_view(),
        name='sponsorshiplevel-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-membershiplevel/$',
        view=SponsorshipLevelCreateView.as_view(),
        name='sponsorshiplevel-create'),
    url(regex='^(?P<project_slug>[\w-]+)/membershiplevel/(?P<slug>[\w-]+)/update/$',
        view=SponsorshipLevelUpdateView.as_view(),
        name='sponsorshiplevel-update'),

    # Sponsorship Period management

    # This view is only accessible via ajax
    url(regex='^json-membershipperiod/list/(?P<version>\d+)/$',
        view=JSONSponsorshipPeriodListView.as_view(),
        name='json-sponsorshipperiod-list'),
    url(regex='^(?P<project_slug>[\w-]+)/pending-membershipperiod/list/$',
        view=PendingSponsorshipPeriodListView.as_view(),
        name='pending-sponsorshipperiod-list'),
    url(regex='^(?P<project_slug>[\w-]+)/approve-membershipperiod/(?P<slug>[\w-]+)/$',
        view=ApproveSponsorshipPeriodView.as_view(),
        name='sponsorshipperiod-approve'),
    url(regex='^(?P<project_slug>[\w-]+)/membershipperiod/list/$',
        view=SponsorshipPeriodListView.as_view(),
        name='sponsorshipperiod-list'),
    url(regex='^(?P<project_slug>[\w-]+)/membershipperiod/(?P<slug>[\w-]+)/$',
        view=SponsorshipPeriodDetailView.as_view(),
        name='sponsorshipperiod-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/membershipperiod/(?P<slug>[\w-]+)/delete/$',
        view=SponsorshipPeriodDeleteView.as_view(),
        name='sponsorshipperiod-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/create-membershipperiod/$',
        view=SponsorshipPeriodCreateView.as_view(),
        name='sponsorshipperiod-create'),
    url(regex='^(?P<project_slug>[\w-]+)/membershipperiod/(?P<slug>[\w-]+)/update/$',
        view=SponsorshipPeriodUpdateView.as_view(),
        name='sponsorshipperiod-update'),

    # Sponsor Cloud
    url(regex='^(?P<project_slug>[\w-]+)/member-cloud/$',
        view=generate_sponsor_cloud,
        name='sponsor-cloud'),

    # Sustaining member
    url(
        regex='^(?P<project_slug>[\w-]+)/sustaining-member/add/$',
        view=SustainingMemberCreateView.as_view(),
        name='sustaining-member-create'),
    url(
        regex='^(?P<project_slug>[\w-]+)/membership/$',
        view=SustainingMembership.as_view(),
        name='sustaining-membership'),
    url(
        regex='^(?P<project_slug>[\w-]+)/sustaining-member/update/'
              '(?P<member_id>\d+)/$',
        view=SustainingMemberUpdateView.as_view(),
        name='sustaining-member-update'),
    url(
        regex='^(?P<project_slug>[\w-]+)/sustaining-member-period/create/'
              '(?P<member_id>\d+)/$',
        view=SustainingMemberPeriodCreateView.as_view(),
        name='sustaining-member-period-create'),
    url(
        regex='^(?P<project_slug>[\w-]+)/sustaining-member-period/update/'
              '(?P<member_id>\d+)/$',
        view=SustainingMemberPeriodUpdateView.as_view(),
        name='sustaining-member-period-update'),
]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT})]
