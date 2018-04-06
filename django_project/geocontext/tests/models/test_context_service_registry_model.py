# coding=utf-8
"""Test for lesson models."""

from django.test import TestCase

from geocontext.models.context_service_registry import ContextServiceRegistry
from geocontext.tests.models.model_factories import ContextServiceRegistryF


class TestContextServiceRegistry(TestCase):
    """Test CSR models."""

    def test_ContextServiceRegistry_create(self):
        """Test section model creation."""

        model = ContextServiceRegistryF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model name exists.
        self.assertTrue(model.name is not None)

    def test_retrieve_context_value(self):
        """Test retrieving context value from a point."""
        x = 27.8
        y = -32.1

        # Case 1, the CRS is same 4326 (query, service)
        model_a = ContextServiceRegistryF.create()
        model_a.url = (
            'http://maps.kartoza.com/web/?map=/web/kartoza/kartoza.qgs')
        model_a.crs = 4326
        model_a.query_type = ContextServiceRegistry.WFS
        model_a.layer_typename = 'water_management_area'
        model_a.service_version = '1.0.0'

        model_a.result_regex = 'qgs:name'

        model_a.save()

        value = model_a.retrieve_context_value(x, y)
        self.assertEqual('12 - Mzimvubu to Keiskamma', value)

        # Case 1, the CRS is different 4326 (query), 3857 (service)
        model_b = ContextServiceRegistryF.create()
        model_b.url = (
            'http://maps.kartoza.com/web/?map=/web/kartoza/kartoza.qgs')
        model_b.crs = 3857
        model_b.query_type = ContextServiceRegistry.WFS
        model_b.layer_typename = 'sa_provinces'
        model_b.service_version = '1.0.0'

        model_b.result_regex = 'qgs:provname'

        model_b.save()

        value = model_b.retrieve_context_value(x, y)
        self.assertEqual('Eastern Cape', value)
