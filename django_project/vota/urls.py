# coding=utf-8
# flake8: noqa

"""Project level url handler."""
from django.conf.urls import patterns, url
from feeds.ballot import BallotFeed
from views.committee import (
    CommitteeDetailView,
    CommitteeCreateView,
    CommitteeUpdateView,
    CommitteeDeleteView,
    CommitteeListView)
from views.vote import VoteCreateUpdateView
from views.ballot import (
    BallotDetailView,
    BallotCreateView,
    BallotDeleteView,
    BallotUpdateView,
    BallotListView
)


urlpatterns = patterns(
    '',
    # Committee URLs
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<slug>[\w-]+)/$',
        view=CommitteeDetailView.as_view(),
        name='committee-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/committees/$',
        view=CommitteeListView.as_view(),
        name='committee-list'),
    url(regex='^(?P<project_slug>[\w-]+)/create-committee/$',
        view=CommitteeCreateView.as_view(),
        name='committee-create'),
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<slug>[\w-]+)/delete/$',
        view=CommitteeDeleteView.as_view(),
        name='committee-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<slug>[\w-]+)/update/$',
        view=CommitteeUpdateView.as_view(),
        name='committee-update'),

    # Voting URLs
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'ballots/(?P<ballot_slug>[\w-]+)/vote/$',
        view=VoteCreateUpdateView.as_view(),
        name='vote-create'),

    # Ballot URLs
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'ballots/(?P<slug>[\w-]+)/$',
        view=BallotDetailView.as_view(),
        name='ballot-detail'),
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'ballots/$',
        view=BallotListView.as_view(),
        name='ballot-list'),
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'ballots/(?P<slug>[\w-]+)/delete/$',
        view=BallotDeleteView.as_view(),
        name='ballot-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'ballots/(?P<slug>[\w-]+)/update/$',
        view=BallotUpdateView.as_view(),
        name='ballot-update'),
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'create-ballot/$',
        view=BallotCreateView.as_view(),
        name='ballot-create'),

    # Feeds
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'ballots-rss/$',
        view=BallotFeed(),
        name='latest-ballot-rss'),
)
