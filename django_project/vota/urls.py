# coding=utf-8
"""Project level url handler."""
from django.conf.urls import patterns, url
from views.committee import CommitteeDetailView, CommitteeCreateView
from views.vote import VoteCreateUpdateView
from views.ballot import BallotDetailView, BallotCreateView


urlpatterns = patterns(
    '',
    ### Committee URLs
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<slug>[\w-]+)/$',
        view=CommitteeDetailView.as_view(),
        name='committee-detail'),
    url(regex='^committee/create/$',
        view=CommitteeCreateView.as_view(),
        name='committee-create'),

    ### Voting URLs
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'ballots/(?P<ballot_slug>[\w-]+)/vote/$',
        view=VoteCreateUpdateView.as_view(),
        name='add-vote'),

    ### Ballot URLs
    url(regex='^(?P<project_slug>[\w-]+)/committees/(?P<committee_slug>[\w-]+)/'
              'ballots/(?P<slug>[\w-]+)/$',
        view=BallotDetailView.as_view(),
        name='ballot-detail'),
    url(regex='^ballot/create/$',
        view=BallotCreateView.as_view(),
        name='ballot-create'),
)
