from rest_framework import serializers
from fish.models import Taxon


class TaxonSerializer(serializers.ModelSerializer):
    """
    Serializer for taxon collection model.
    """
    iucn_status_sensitive = serializers.SerializerMethodField()
    iucn_status_name = serializers.SerializerMethodField()

    def get_iucn_status_sensitive(self, obj):
        return obj.iucn_status.sensitive

    def get_iucn_status_name(self, obj):
        return obj.iucn_status.name

    class Meta:
        model = Taxon
        fields = '__all__'
