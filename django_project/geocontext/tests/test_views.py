# coding=utf-8
"""Test views."""

from django.test import TestCase
from datetime import datetime

from geocontext.tests.models.model_factories import ContextServiceRegistryF
from geocontext.models.context_service_registry import ContextServiceRegistry

from geocontext.views import retrieve_context


class TestGeoContextView(TestCase):
    """Test for geocontext view."""

    def test_cache_retrieval(self):
        """Test for retrieving from service registry and cache."""
        x = 27.8
        y = -32.1

        service_registry = ContextServiceRegistryF.create()
        service_registry.url = (
            'http://maps.kartoza.com/web/?map=/web/kartoza/kartoza.qgs')
        service_registry.srid = 4326
        service_registry.query_type = ContextServiceRegistry.WFS
        service_registry.layer_typename = 'water_management_area'
        service_registry.service_version = '1.0.0'

        service_registry.result_regex = 'qgs:name'

        service_registry.save()

        start_direct = datetime.now()
        retrieve_context(x, y, service_registry.name)
        end_direct = datetime.now()

        start_cache = datetime.now()
        retrieve_context(x, y, service_registry.name)
        end_cache = datetime.now()

        duration_direct = end_direct - start_direct
        duration_cache = end_cache - start_cache
        message = 'Direct: %.5f. Cache: %.5f' % (
            duration_direct.total_seconds(), duration_cache.total_seconds())
        print(message)
        self.assertGreater(duration_direct, duration_cache, message)
