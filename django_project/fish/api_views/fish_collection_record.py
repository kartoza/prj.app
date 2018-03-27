# coding=utf8
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from fish.models.fish_collection_record import FishCollectionRecord
from fish.serializers.fish_collection_serializer import \
    FishCollectionSerializer


class FishCollectionList(APIView):
    """
    List all fish collection.
    """

    def get(self, request, *args):
        fish_collections = FishCollectionRecord.objects.all()
        serializer = FishCollectionSerializer(fish_collections, many=True)
        return Response(serializer.data)


class FishCollectionDetail(APIView):
    """
    Retrieve a fish collection instance.
    """

    def get_object(self, pk):
        try:
            return FishCollectionRecord.objects.get(pk=pk)
        except FishCollectionRecord.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        fish_collection = self.get_object(pk)
        serializer = FishCollectionSerializer(fish_collection)
        return Response(serializer.data)
