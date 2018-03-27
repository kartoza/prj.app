# coding=utf-8

from django.contrib import admin
from fish.models import (
    FishCollectionRecord,
    IUCNStatus,
    Taxon,
    CSVDocument
)


class IUCNStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'sensitive')


class TaxonAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'author', 'iucn_status')


class FishCollectionAdmin(admin.ModelAdmin):
    list_display = (
        'original_species_name',
        'habitat',
        'category',
        'collection_date',
        'owner',
    )


admin.site.register(FishCollectionRecord, FishCollectionAdmin)
admin.site.register(IUCNStatus, IUCNStatusAdmin)
admin.site.register(Taxon, TaxonAdmin)
admin.site.register(CSVDocument)
