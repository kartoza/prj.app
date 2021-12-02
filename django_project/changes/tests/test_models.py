# coding=utf-8
"""Tests for models."""
from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from changes.tests.model_factories import (
    CategoryF,
    EntryF,
    VersionF,
    SponsorshipLevelF,
    SponsorF,
    SponsorshipPeriodF)
from base.tests.model_factories import ProjectF


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
        model = CategoryF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_Category_read(self):
        """
        Tests Category model read
        """
        model = CategoryF.create(
            name=u'Custom Category'
        )

        self.assertTrue(model.name == 'Custom Category')
        self.assertTrue(model.slug == 'custom-category')

    def test_Category_update(self):
        """
        Tests Category model update
        """
        model = CategoryF.create()
        new_model_data = {
            'name': u'New Category Name',
            'description': u'New description',
            'private': True,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Category_delete(self):
        """
        Tests Category model delete
        """
        model = CategoryF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


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
        model = EntryF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.title is not None)

    def test_Entry_read(self):
        """
        Tests Entry model read
        """
        model = EntryF.create(
            title=u'Custom Entry',
            developed_by=u'Tim'
        )

        self.assertTrue(model.title == 'Custom Entry')
        self.assertTrue(model.slug == 'custom-entry')
        self.assertTrue(model.developer_info_html() == '')

        model = EntryF.create(
            title=u'Custom Entry',
            developed_by=u'Tim',
            developer_url=''
        )
        self.assertTrue(
            model.developer_info_html() == 'This feature was '
                                           'developed by Tim ')

        model = EntryF.create(
            title=u'Custom Entry',
            developed_by=u'Tim',
            developer_url=u'https://github.com/timlinux'
        )
        self.assertTrue(
            model.developer_info_html() == 'This feature was '
                                           'developed by [Tim]'
                                           '(https://github.com/timlinux)')

    def test_Entry_update(self):
        """
        Tests Entry model update
        """
        model = EntryF.create()
        new_model_data = {
            'name': u'New Entry Name',
            'description': u'New description',
            'approved': False,
            'private': True,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Entry_delete(self):
        """
        Tests Entry model delete
        """
        model = EntryF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


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
        model = VersionF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_Version_read(self):
        """
        Tests Version model read
        """
        model = VersionF.create(
            description=u'Test Description'
        )
        self.assertTrue(model.description == 'Test Description')

    def test_Version_update(self):
        """
        Tests Version model update
        """
        model = VersionF.create()
        new_model_data = {
            '10002001': u'10002001',
            'description': u'New description',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_formatted_release_date(self):
        """Tests we can get, set and present the release date nicely."""
        model = VersionF.create(
            description=u'New description',
            release_date=datetime(2016, 6, 6),
        )
        self.assertEquals(model.formatted_release_date(), '6 June, 2016')

    def test_Version_delete(self):
        """
        Tests Version model delete
        """
        model = VersionF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestVersionSponsors(TestCase):
    """
    Tests that we can filter sponsors for a version.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Version_Sponsors(self):
        """
        Tests version sponsors
        """
        project = ProjectF.create()

        sponsorship_period = SponsorshipPeriodF.create()
        data = {
            'start_date': datetime(2016, 1, 1).date(),
            'end_date': datetime(2016, 2, 1).date(),
            'approved': True,
            'private': False,
            'project_id': project.pk,
        }
        sponsorship_period.__dict__.update(data)
        sponsorship_period.save()

        version_model = VersionF.create()
        data = {
            '10002001': u'10002001',
            'description': u'New description',
            'approved': True,
            'release_date': datetime(2016, 1, 10).date(),
            'project_id': project.pk,
        }
        version_model.__dict__.update(data)
        version_model.save()

        version_model.refresh_from_db()
        sponsors = version_model.sponsors()
        self.assertEqual(sponsors.count(), 1)


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
        model = SponsorF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_Sponsor_read(self):
        """
        Tests Sponsor model read
        """
        model = SponsorF.create(
            name=u'Custom Sponsor'
        )

        self.assertTrue(model.name == 'Custom Sponsor')

    def test_Sponsor_update(self):
        """
        Tests Sponsor model update
        """
        model = SponsorF.create()
        new_model_data = {
            'name': u'New Sponsor Name',
            'sponsor_url': u'New Sponsor URL',
            'approved': False,
            'private': True,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Sponsor_delete(self):
        """
        Tests Sponsor model delete
        """
        model = SponsorF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


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
        model = SponsorshipLevelF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_SponsorshipLevel_read(self):
        """
        Tests Sponsorship Level model read
        """
        model = SponsorshipLevelF.create(
            name=u'Custom SponsorshipLevel'
        )

        self.assertTrue(model.name == 'Custom SponsorshipLevel')

    def test_SponsorshipLevel_update(self):
        """
        Tests Sponsorship Level model update
        """
        model = SponsorshipLevelF.create()
        new_model_data = {
            'name': u'New Sponsorship Level Name',
            'currency': u'IDR',
            'approved': False,
            'private': True,
            'logo_width': 100,
            'logo_height': 100
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_SponsorshipLevel_delete(self):
        """
        Tests SponsorshipLevel model delete
        """
        model = SponsorshipLevelF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


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
        model = SponsorshipPeriodF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.start_date is not None)

    def test_SponsorshipPeriod_read(self):
        """
        Tests Sponsorship Period model read
        """
        model = SponsorshipPeriodF.create(
            start_date=datetime(2016, 1, 1)
        )

        self.assertTrue(model.start_date == datetime(2016, 1, 1))

    def test_SponsorshipPeriod_update(self):
        """
        Tests Sponsorship Period model update
        """
        model = SponsorshipPeriodF.create()
        new_model_data = {
            'start_date': datetime(2016, 1, 1),
            'approved': False,
            'private': True,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_SponsorshipPeriod_delete(self):
        """
        Tests SponsorshipPeriod model delete
        """
        model = SponsorshipPeriodF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestValidateEmailAddress(TestCase):
    """Test validate_email_address function."""

    def test_validation_failed_must_raise_ValidationError(self):
        from changes.models import validate_email_address
        email = 'email@wrongdomain'
        msg = f'{email} is not a valid email address'
        with self.assertRaisesMessage(ValidationError, msg):
            validate_email_address(email)
