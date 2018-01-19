# coding=utf-8
"""Test for lesson models."""

from django.test import TestCase

from lesson.tests.model_factories import (
    SpecificationF,
)


class TestSpecification(TestCase):
    """Test specification models."""

    def setUp(self):
        """Set up before each test."""

        pass

    def test_Specification_create(self):
        """Test specification model creation."""

        model = SpecificationF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model title exists.
        self.assertTrue(model.title is not None)

    def test_Specification_delete(self):
        """Test specification model deletion."""

        model = SpecificationF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)

    def test_Specification_read(self):
        """Test specification model read."""

        model = SpecificationF.create(
            title=u'Title 1',
            value=u'Value 1',
            notes=u'Notes 1'
        )

        self.assertTrue(model.title == 'Title 1')

    def test_Specification_update(self):
        """Test specification on update."""

        model = SpecificationF.create()
        new_model_data = {
            'title': u'new title',
            'value': u'new value',
            'notes': u'new notes'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)
