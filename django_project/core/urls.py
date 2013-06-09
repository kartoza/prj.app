from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    # url(r'^visual_changelogger/', include('visual_changelogger.foo.urls')),
)
