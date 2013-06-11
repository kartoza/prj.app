from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', RedirectView.as_view(url='/entry/list')),
    url(r'^', include('changes.urls')),
)
