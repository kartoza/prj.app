# coding=utf-8
"""Tests for models."""
from django.test import TestCase
from changes.tests.model_factories import CategoryF, EntryF, VersionF


class TestCategoryCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Category_create(self):
        """
        Tests Category model creation
        """
        my_model = CategoryF.create()

        #check if PK exists
        self.assertTrue(my_model.pk is not None)

        #check if name exists
        self.assertTrue(my_model.name is not None)

    def test_Category_read(self):
        """
        Tests Category model read
        """
        my_model = CategoryF.create(
            name=u'Custom Category'
        )

        self.assertTrue(my_model.name == 'Custom Category')
        self.assertTrue(my_model.slug == 'custom-category')

    def test_Category_update(self):
        """
        Tests Category model update
        """
        my_model = CategoryF.create()
        new_model_data = {
            'name': u'New Category Name',
            'description': u'New description',
            'approved': False,
            'private': True,
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        #check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Category_delete(self):
        """
        Tests Category model delete
        """
        my_model = CategoryF.create()

        my_model.delete()

        #check if deleted
        self.assertTrue(my_model.pk is None)


class TestEntryCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Entry_create(self):
        """
        Tests Entry model creation
        """
        my_model = EntryF.create()

        #check if PK exists
        self.assertTrue(my_model.pk is not None)

        #check if name exists
        self.assertTrue(my_model.title is not None)

    def test_Entry_read(self):
        """
        Tests Entry model read
        """
        my_model = EntryF.create(
            title=u'Custom Entry'
        )

        self.assertTrue(my_model.title == 'Custom Entry')
        self.assertTrue(my_model.slug == 'custom-entry')

    def test_Entry_update(self):
        """
        Tests Entry model update
        """
        my_model = EntryF.create()
        new_model_data = {
            'name': u'New Entry Name',
            'description': u'New description',
            'approved': False,
            'private': True,
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        #check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Entry_delete(self):
        """
        Tests Entry model delete
        """
        my_model = EntryF.create()

        my_model.delete()

        #check if deleted
        self.assertTrue(my_model.pk is None)


class TestVersionCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Version_create(self):
        """
        Tests Version model creation
        """
        my_model = VersionF.create()

        #check if PK exists
        self.assertTrue(my_model.pk is not None)

        #check if name exists
        self.assertTrue(my_model.name is not None)

    def test_Version_read(self):
        """
        Tests Version model read
        """
        my_model = VersionF.create(
            name=u'Custom Version'
        )

        self.assertTrue(my_model.name == 'Custom Version')
        self.assertTrue(my_model.slug == 'custom-version')

    def test_Version_update(self):
        """
        Tests Version model update
        """
        my_model = VersionF.create()
        new_model_data = {
            'name': u'New Version Name',
            'description': u'New description',
            'approved': True
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        #check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Version_delete(self):
        """
        Tests Version model delete
        """
        my_model = VersionF.create()

        my_model.delete()

        #check if deleted
        self.assertTrue(my_model.pk is None)
