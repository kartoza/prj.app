from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('changes.urls')),
    url(r'^accounts/', include('userena.urls')),
)
