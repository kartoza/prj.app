# coding=utf-8
"""Tests for models."""
from django.test import TestCase
from changes.tests.model_factories import CategoryF, EntryF, VersionF, SponsorshipLevelF, SponsorF, SponsorshipPeriodF


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

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if name exists
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

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Category_delete(self):
        """
        Tests Category model delete
        """
        my_model = CategoryF.create()

        my_model.delete()

        # check if deleted
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

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if name exists
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

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Entry_delete(self):
        """
        Tests Entry model delete
        """
        my_model = EntryF.create()

        my_model.delete()

        # check if deleted
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

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if name exists
        self.assertTrue(my_model.name is not None)

    def test_Version_read(self):
        """
        Tests Version model read
        """
        my_model = VersionF.create(
            description=u'Test Description'
        )
        self.assertTrue(my_model.description == 'Test Description')

    def test_Version_update(self):
        """
        Tests Version model update
        """
        my_model = VersionF.create()
        new_model_data = {
            '10002001': u'10002001',
            'description': u'New description',
            'approved': True
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Version_delete(self):
        """
        Tests Version model delete
        """
        my_model = VersionF.create()

        my_model.delete()

        # check if deleted
        self.assertTrue(my_model.pk is None)


class TestSponsorCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Sponsor_create(self):
        """
        Tests Sponsor model creation
        """
        my_model = SponsorF.create()

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if name exists
        self.assertTrue(my_model.name is not None)

    def test_Sponsor_read(self):
        """
        Tests Sponsor model read
        """
        my_model = SponsorF.create(
            name=u'Custom Sponsor'
        )

        self.assertTrue(my_model.name == 'Custom Sponsor')

    def test_Sponsor_update(self):
        """
        Tests Sponsor model update
        """
        my_model = SponsorF.create()
        new_model_data = {
            'name': u'New Sponsor Name',
            'sponsor_url': u'New Sponsor URL',
            'approved': False,
            'private': True,
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Sponsor_delete(self):
        """
        Tests Sponsor model delete
        """
        my_model = SponsorF.create()

        my_model.delete()

        # check if deleted
        self.assertTrue(my_model.pk is None)


class TestSponsorshipLevelCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SponsorshipLevel_create(self):
        """
        Tests Sponsorship Level model creation
        """
        my_model = SponsorshipLevelF.create()

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if name exists
        self.assertTrue(my_model.name is not None)

    def test_SponsorshipLevel_read(self):
        """
        Tests Sponsorship Level model read
        """
        my_model = SponsorshipLevelF.create(
            name=u'Custom SponsorshipLevel'
        )

        self.assertTrue(my_model.name == 'Custom SponsorshipLevel')

    def test_SponsorshipLevel_update(self):
        """
        Tests Sponsorship Level model update
        """
        my_model = SponsorshipLevelF.create()
        new_model_data = {
            'name': u'New Sponsorship Level Name',
            'currency': u'IDR',
            'approved': False,
            'private': True,
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)


class TestSponsorshipPeriodCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_SponsorshipPeriod_create(self):
        """
        Tests Sponsorship Period model creation
        """
        my_model = SponsorshipPeriodF.create()

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if name exists
        self.assertTrue(my_model.start_date is not None)

    def test_SponsorshipPeriod_read(self):
        """
        Tests Sponsorship Period model read
        """
        my_model = SponsorshipPeriodF.create(
            start_date= u'2016-01-01'
        )

        self.assertTrue(my_model.start_date == '2016-01-01')

    def test_SponsorshipPeriod_update(self):
        """
        Tests Sponsorship Period model update
        """
        my_model = SponsorshipPeriodF.create()
        new_model_data = {
            'start_date': u'2016-01-01',
            'approved': False,
            'private': True,
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)
