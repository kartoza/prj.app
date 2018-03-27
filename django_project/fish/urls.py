# coding=utf-8

from django.conf.urls import url
from fish.views.csv_upload import CsvUploadView
from fish.api_views.fish_collection_record import (
    FishCollectionList,
    FishCollectionDetail,
)
from fish.api_views.taxon import TaxonDetail


api_urls = [
    url(r'^api/fish-collections/$', FishCollectionList.as_view()),
    url(r'^api/fish-collections/(?P<pk>[0-9]+)/$',
        FishCollectionDetail.as_view()),
    url(r'^api/taxon/(?P<pk>[0-9]+)/$',
        TaxonDetail.as_view()),
]

urlpatterns = [
    url(regex=r'^csv_uploader/$',
        view=CsvUploadView.as_view(),
        name='csv-upload'),
] + api_urls
