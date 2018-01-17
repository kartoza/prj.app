# coding=utf-8
"""Test for lesson models."""

from django.test import TestCase

from lesson.tests.model_factories import (
    SectionF
)


class TestSection(TestCase):
    """Test section models."""

    def setUp(self):
        """Set up before each test."""

        pass

    def test_Section_create(self):
        """Test section model creation."""

        model = SectionF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model name exists.
        self.assertTrue(model.name is not None)

    def test_Section_delete(self):
        """Test section model deletion."""

        model = SectionF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)

    def test_Section_read(self):
        """Test section model read."""

        model = SectionF.create(
            name=u'Section Introduction'
        )

        self.assertTrue(model.name == 'Section Introduction')

    def test_Section_update(self):
        """Test section update."""

        model = SectionF.create()
        new_model_data = {
            'name': u'new section name',
            'notes': u'new notes for sure'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)
