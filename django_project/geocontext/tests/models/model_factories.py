# coding=utf-8
"""Factories for building model instances for testing."""

import factory
from geocontext.models.context_service_registry import ContextServiceRegistry


class ContextServiceRegistryF(factory.DjangoModelFactory):
    class Meta:
        model = ContextServiceRegistry

    name = factory.sequence(
        lambda n: u'Test CSR name %s' % n)
    display_name = factory.sequence(
        lambda n: u'Test CSR display name %s' % n)
    description = factory.sequence(
        lambda n: u'Test CSR description %s' % n)
