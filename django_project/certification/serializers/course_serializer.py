# coding=utf-8
from rest_framework import serializers
from ..models.course import Course
from .rest_framework_gis.serializers import GeoFeatureModelSerializer
from .rest_framework_gis.fields import GeometrySerializerMethodField


class CourseSerializer(GeoFeatureModelSerializer):
    """ A class to serialize courses as GeoJSON data."""

    location = GeometrySerializerMethodField()
    course_type_name = serializers.SerializerMethodField()
    course_convener_name = serializers.SerializerMethodField()
    training_center_name = serializers.SerializerMethodField()
    certifying_organisation_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        geo_field = 'location'
        fields = [
            'name',
            'start_date',
            'end_date',
            'course_type_name',
            'course_convener_name',
            'training_center_name',
            'certifying_organisation_name',
            'language',
            'trained_competence'
        ]

    def get_location(self, obj):
        return obj.location

    def get_course_type_name(self, obj):
        return obj.course_type.name

    def get_course_convener_name(self, obj):
        return obj.course_convener.full_name

    def get_training_center_name(self, obj):
        return obj.training_center.name

    def get_certifying_organisation_name(self, obj):
        return obj.certifying_organisation.name
