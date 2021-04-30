# coding=utf-8
"""Factories for building model instances for testing."""

import factory

from base.tests.model_factories import ProjectF

from lesson.models import (
    FurtherReading,
    License,
    Section,
    Specification,
    Worksheet,
)


class SectionF(factory.django.DjangoModelFactory):
    """Section model factory."""

    class Meta:
        model = Section

    name = factory.sequence(
        lambda n: u'Test section name %s' % n)
    notes = factory.sequence(
        lambda n: u'Test section notes %s' % n)
    project = factory.SubFactory(ProjectF)


class WorksheetF(factory.django.DjangoModelFactory):
    """Worksheet model factory."""

    class Meta:
        model = Worksheet

    section = factory.SubFactory(SectionF)
    module = factory.sequence(
        lambda n: u'Test module %s' % n)
    title = factory.sequence(
        lambda n: u'Test title %s' % n)
    summary_leader = factory.sequence(
        lambda n: u'Summary leader %s' % n)
    summary_text = factory.sequence(
        lambda n: u'Summary text %s' % n)
    summary_image = factory.sequence(
        lambda n: u'Summary_image %s' % n)
    exercise_task = factory.sequence(
        lambda n: u'Exercise task %s' % n)
    more_about_text = factory.sequence(
        lambda n: u'More about text %s' % n)
    more_about_image = factory.sequence(
        lambda n: u'More about image %s' % n)


class SpecificationF(factory.django.DjangoModelFactory):
    """Specification model factory."""

    class Meta:
        model = Specification

    worksheet = factory.SubFactory(WorksheetF)
    title = factory.sequence(
        lambda n: u'Test title %s' % n)
    value = factory.sequence(
        lambda n: u'Test value %s' % n)
    title_notes = factory.sequence(
        lambda n: u'Test section title notes %s' % n)
    value_notes = factory.sequence(
        lambda n: u'Test section value notes %s' % n)


class LicenseF(factory.django.DjangoModelFactory):
    """License model factory"""

    class Meta:
        model = License

    name = 'Test License'
    file = factory.django.FileField(byte=b'test license content')


class FurtherReadingF(factory.django.DjangoModelFactory):
    """Further Reading model factory."""

    class Meta:
        model = FurtherReading

    text = ('Test Further Reading. <a href="https://github.com/kartoza/'
            'prj.app">Projecta Repository</a>')
    worksheet = factory.SubFactory(WorksheetF)
