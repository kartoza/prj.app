# coding=utf-8
"""Project level url handler."""
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    # Enable the admin (use non standard name for obscurity)
    url(r'^site-admin/', include(admin.site.urls)),
    url(r'^', include('base.urls')),
    url(r'^', include('changes.urls')),
    url(r'^(?P<projectSlug>[\w-]+)/', include('vota.urls')),
    url(r'^', include('github_issue.urls')),
    url(r'^accounts/', include('userena.urls')),
)
