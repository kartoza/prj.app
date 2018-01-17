# coding=utf-8
"""Factories for building model instances for testing."""

import factory

from base.tests.model_factories import ProjectF

from lesson.models import (
    Section
)


class SectionF(factory.django.DjangoModelFactory):
    """Section model factory"""

    class Meta:
        model = Section

    name = factory.sequence(
        lambda n: u'Test section name %s' % n)
    notes = factory.sequence(
        lambda n: u'Test section notes %s' % n)
    project = factory.SubFactory(ProjectF)
