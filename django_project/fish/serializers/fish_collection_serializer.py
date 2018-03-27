from rest_framework import serializers
from fish.models import FishCollectionRecord


class FishCollectionSerializer(serializers.ModelSerializer):
    """
    Serializer for fish collection model.
    """
    owner = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return '%s,%s' % (obj.owner.pk, obj.owner.username)

    def get_geometry(self, obj):
        return obj.site.get_geometry().json

    class Meta:
        model = FishCollectionRecord
        fields = '__all__'
