# coding=utf-8

from django.contrib.gis import admin
from base.models import (
    LocationType,
    LocationSite,
)


class LocationSiteAdmin(admin.GeoModelAdmin):
    default_zoom = 5
    default_lat = -30
    default_lon = 25


admin.site.register(LocationSite, LocationSiteAdmin)
admin.site.register(LocationType)
