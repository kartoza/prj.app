# coding=utf-8
"""Test for lesson models."""

from django.test import TestCase
from django.utils import translation

from lesson.tests.model_factories import WorksheetF


class TestSection(TestCase):
    """Test section models."""

    def test_Worksheet_create(self):
        """Test worksheet model creation."""

        model = WorksheetF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model title exists.
        self.assertTrue(model.title is not None)

        # check if __str__ method returns the correct value
        self.assertEqual(str(model), model.module)

        # check if published default False
        self.assertFalse(model.published)

    def test_Worksheet_delete(self):
        """Test worksheet model deletion."""

        model = WorksheetF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)

    def test_Worksheet_read(self):
        """Test worksheet model read."""

        model = WorksheetF.create(
            module=u'Worksheet 1',
            title=u'Title 1',
            summary_leader=u'Summary Leader 1',
            summary_text=u'Summary Text 1',
            exercise_goal=u'Goal 1',
            exercise_task=u'Task 1',
            more_about_text=u'More info'
        )

        self.assertTrue(model.title == 'Title 1')

    def test_Worksheet_update(self):
        """Test worksheet on update."""

        model = WorksheetF.create()
        new_model_data = {
            'module': u'new module name',
            'title': u'new title for sure',
            'summary_leader': u'checkout my new summary !',
            'summary_text': u'my new text',
            'summary_image': u'new fake pic',
            'exercise_goal': u'new goal',
            'exercise_task': u'new task',
            'more_about_text': u'new more text',
            'more_about_image': u'new more image',
            'published': True,
            'page_break_before_exercise': True,
            'page_break_before_requirement_table': True,
            'page_break_before_exercise_image': True,
            'page_break_before_more_about': True,
            'page_break_before_question': True,
            'page_break_before_youtube_link': True,
            'page_break_before_further_reading': True
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Worksheet_update_last_update(self):
        """Test worksheet on translation update."""
        indonesian_title = 'Judul Baru.'

        model = WorksheetF.create()
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
