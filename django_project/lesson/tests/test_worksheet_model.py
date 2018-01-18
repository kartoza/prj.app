# coding=utf-8
"""Test for lesson models."""

from django.test import TestCase

from lesson.tests.model_factories import (
    WorksheetF,
)


class TestSection(TestCase):
    """Test section models."""

    def setUp(self):
        """Set up before each test."""

        pass

    def test_Worksheet_create(self):
        """Test worksheet model creation."""

        model = WorksheetF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model title exists.
        self.assertTrue(model.title is not None)

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
            'more_about_image': u'new more image'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)
