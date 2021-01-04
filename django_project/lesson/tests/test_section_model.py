# coding=utf-8
"""Test for lesson models."""

from django.test import TestCase
from django.utils import translation

from lesson.tests.model_factories import SectionF


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

        # check if __str__ method returns the correct value
        self.assertEqual(str(model), model.name)

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

    def test_Section_update_last_update(self):
        """Test section on translation update."""
        indonesian_name = 'Name Baru.'

        model = SectionF.create()
        last_update = model.last_update
        model.name = 'New name please'
        model.save()
        self.assertTrue(last_update < model.last_update)

        with translation.override('id'):
            # At first it's not up to date
            self.assertFalse(model.is_translation_up_to_date)
            # Update the name in Bahasa Indonesia
            model.name = indonesian_name
            model.save()
            # It should be up to date.
            self.assertTrue(model.is_translation_up_to_date)

        # Update the English one
        model.name = 'New name 2'
        model.save()

        with translation.override('id'):
            # It becomes not up to date again.
            self.assertFalse(model.is_translation_up_to_date)
            self.assertEqual(indonesian_name, model.name)
            # Update the name in Bahasa Indonesia
            model.name = 'Nama Baru 2.'
            model.save()
            # It should be up to date.
            self.assertTrue(model.is_translation_up_to_date)
