# coding=utf-8
"""Test for lesson models."""

from django.test import TestCase
from django.utils import translation

from lesson.tests.model_factories import SpecificationF


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

        # check if __str__ method returns the correct value
        self.assertEqual(str(model), model.title)

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
            title_notes=u'Notes 1',

        )

        self.assertTrue(model.title == 'Title 1')

    def test_Specification_update(self):
        """Test specification on update."""

        model = SpecificationF.create()
        new_model_data = {
            'title': u'new title',
            'value': u'new value',
            'title_notes': u'new notes'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Specification_update_last_update(self):
        """Test specification on translation update."""
        indonesian_title = 'Judul Baru.'

        model = SpecificationF.create()
        last_update = model.last_update
        model.title = 'New title please'
        model.save()
        self.assertTrue(last_update < model.last_update)

        with translation.override('id'):
            # At first it's not up to date
            self.assertFalse(model.is_translation_up_to_date)
            # Update the title in Bahasa Indonesia
            model.title = indonesian_title
            model.save()
            # It should be up to date.
            self.assertTrue(model.is_translation_up_to_date)

        # Update the English one
        model.title = 'New title 2'
        model.save()

        with translation.override('id'):
            # It becomes not up to date again.
            self.assertFalse(model.is_translation_up_to_date)
            self.assertEqual(indonesian_title, model.title)
            # Update the title in Bahasa Indonesia
            model.title = 'Judul Baru 2.'
            model.save()
            # It should be up to date.
            self.assertTrue(model.is_translation_up_to_date)
