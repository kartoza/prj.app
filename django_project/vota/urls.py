# coding=utf-8
"""Project level url handler."""
from django.conf.urls import patterns, url
from views.committee import CommitteeDetailView
from views.vote import VoteCreateUpdateView
from views.ballot import BallotDetailView


urlpatterns = patterns(
    '',
    ### Committee URLs
    url(regex='^(?P<slug>[\w-]+)/$',
        view=CommitteeDetailView.as_view(),
        name='committee-detail'),

    ### Voting URLs
    url(regex='^(?P<committee_slug>[\w-]+)/ballots/'
              '(?P<ballot_slug>[\w-]+)/vote/$',
        view=VoteCreateUpdateView.as_view(),
        name='add-vote'),

    ### Ballot URLs
    url(regex='^(?P<committee_slug>[\w-]+)/ballots/(?P<slug>[\w-]+)/$',
        view=BallotDetailView.as_view(),
        name='ballot-detail'),
)
