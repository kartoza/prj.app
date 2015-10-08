# coding=utf-8
"""Project level url handler."""
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

handler404 = 'base.views.error_views.custom_404'

# noinspection PyUnresolvedReferences
urlpatterns = patterns(
    '',
    # Enable the admin (use non standard name for obscurity)
    url(r'^site-admin/', include(admin.site.urls)),
    url(r'^', include('base.urls')),
    url(r'^', include('changes.urls')),
    url(r'^', include('vota.urls')),
    url(r'^', include('github_issue.urls')),

    # This over-ride is required to fix 500 errors as per:
    # https://github.com/bread-and-pepper/django-userena/issues/380
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'userena/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^accounts/', include('userena.urls')),
)
