# coding=utf-8
"""Tests for models."""
from django.test import TestCase
from django.contrib.gis.geos import LineString
from django.core.exceptions import ValidationError
from base.tests.model_factories import LocationTypeF, LocationSiteF


class TestLocationTypeCRUD(TestCase):
    """
    Tests location type.
    """
    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_LocationType_create(self):
        """
        Tests location type creation
        """
        model = LocationTypeF.create()

        # check if pk exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

        # check if description exists
        self.assertTrue(model.description is not None)

    def test_LocationType_read(self):
        """
        Tests location type model read
        """
        model = LocationTypeF.create(
            name=u'custom location',
            description=u'custom description',
        )

        self.assertTrue(model.name == 'custom location')
        self.assertTrue(model.description == 'custom description')

    def test_LocationType_update(self):
        """
        Tests location type model update
        """
        model = LocationTypeF.create()
        new_data = {
            'name': u'new name',
            'description': u'new description'
        }
        model.__dict__.update(new_data)
        model.save()

        # check if updated
        for key, val in new_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_LocationType_delete(self):
        """
        Tests location type model delete
        """
        model = LocationTypeF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestLocationSiteCRUD(TestCase):
    """
    Tests location site.
    """
    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_LocationSite_create(self):
        """
        Tests location site creation
        """
        model = LocationSiteF.create()

        # check if pk exists
        self.assertTrue(model.pk is not None)

        # check if location_type exists
        self.assertTrue(model.location_type is not None)

        # check if geometry exists
        self.assertTrue(model.geometry_point is not None)

    def test_LocationSite_read(self):
        """
        Tests location site model read
        """
        location_type = LocationTypeF.create(
            name=u'custom type',
        )
        model = LocationSiteF.create(
            location_type=location_type
        )

        self.assertTrue(model.location_type.name == 'custom type')

    def test_LocationSite_update(self):
        """
        Tests location site model update
        """
        location_type = LocationTypeF.create(
                name=u'custom type',
        )
        model = LocationSiteF.create()
        new_data = {
            'location_type': location_type,
        }
        model.__dict__.update(new_data)
        model.save()

        # check if updated
        for key, val in new_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_LocationSite_delete(self):
        """
        Tests location site model delete
        """
        model = LocationSiteF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_LocationSite_update_not_in_allowed_geometry(self):
        """
        Tests location site model update if geometry is not in allowed
        geometry
        """
        location_site = LocationSiteF.create()
        new_data = {
            'geometry_point': None,
            'geometry_line': LineString((1, 1), (2, 2)),
        }
        location_site.__dict__.update(new_data)

        # check if validation error raised
        self.assertRaises(ValidationError, location_site.save)
