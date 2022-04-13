from django.test import TestCase

from certification.serializers.course_serializer import CourseSerializer
from certification.tests.model_factories import CourseF, CourseTypeF


class TestSerializer(TestCase):
    """Test certifying organisation serializer."""

    def test_course_serializer(self):
        course_type = CourseTypeF.create(
            name='test_course_type'
        )
        course = CourseF.create(
            course_type=course_type
        )
        serializer = CourseSerializer(course, many=False)
        serializer_data = dict(
            serializer.data['properties']
        )
        self.assertEqual(
            serializer_data['course_type_name'],
            'test_course_type'
        )
