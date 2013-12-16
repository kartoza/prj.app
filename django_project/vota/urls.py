# coding=utf-8
"""Project level url handler."""
from django.conf.urls import patterns, url
from views.committee import CommitteeDetailView
from views.vote import VoteCreateView


urlpatterns = patterns(
    '',
    # basic app views
    # url(regex='^$',
    #     view=ProjectListView.as_view(),
    #     name='home'),
    # # Project management
    # url(regex='^pending-project/list/$',
    #     view=PendingProjectListView.as_view(),
    #     name='pending-project-list'),
    # url(regex='^approve-project/(?P<pk>\d+)/$',
    #     view=ApproveProjectView.as_view(),
    #     name='project-approve'),
    # url(regex='^project/list/$',
    #     view=ProjectListView.as_view(),
    #     name='project-list'),
    url(regex='^committee/(?P<pk>\d+)/$',
        view=CommitteeDetailView.as_view(),
        name='committee-detail'),
    # url(regex='^project/delete/(?P<pk>\d+)/$',
    #     view=ProjectDeleteView.as_view(),
    #     name='project-delete'),
    # url(regex='^project/create/$',
    #     view=ProjectCreateView.as_view(),
    #     name='project-create'),
    # url(regex='^project/update/(?P<pk>\d+)/$',
    #     view=ProjectUpdateView.as_view(),
    #     name='project-update'),


    ### VOTING URLs
    url(regex='^ballot/(?P<ballotID>\d+)/vote/$',
        view=VoteCreateView.as_view(),
        name='add-vote'),
)
