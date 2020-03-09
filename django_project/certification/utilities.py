# coding=utf-8
"""Tools for Certification app."""
from django.contrib.gis.serializers.geojson import Serializer


def check_slug(queryset, slug):
    """
    This function checks slug within a model queryset
    and return a new incremented slug when there are duplicates.

    """

    registered_slug = queryset.values_list('slug', flat=True)
    new_slug = slug
    if slug in registered_slug:
        match_slug = [s for s in registered_slug if slug in s]
        num = len(match_slug)
        new_slug = str(num) + '-' + slug

    return new_slug


class CustomSerializer(Serializer):

    def end_object(self, obj):
        for field in self.selected_fields:
            if field == 'pk':
                continue
            elif field in self._current.keys():
                continue
            else:
                try:
                    if '__' in field:
                        fields = field.split('__')
                        value = obj
                        for f in fields:
                            value = getattr(value, f)
                        if value != obj:
                            self._current[field] = value

                except AttributeError:
                    pass
        super(CustomSerializer, self).end_object(obj)