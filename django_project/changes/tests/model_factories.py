# coding=utf-8
"""Factories for creating model instances for testing."""

import factory
import factory.fuzzy
from datetime import datetime, timedelta, date
from changes.models.category import Category
from changes.models.entry import Entry
from changes.models.version import Version
from changes.models.sponsorship_level import SponsorshipLevel
from changes.models.sponsor import Sponsor
from changes.models.sponsorship_period import SponsorshipPeriod
from core.model_factories import UserF


class CategoryF(factory.django.DjangoModelFactory):
    """
    Category model factory
    """
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: u'Test Category %s' % n)
    sort_number = factory.Sequence(lambda n: n)
    project = factory.SubFactory('base.tests.model_factories.ProjectF')


class EntryF(factory.django.DjangoModelFactory):
    """
    Entry model factory
    """
    class Meta:
        model = Entry

    title = factory.Sequence(lambda n: u'This is a great title: %s' % n)
    description = u'This description is really only here for testing'
    image_file = factory.django.ImageField(color='blue')
    image_credits = u'The credits go to dodobas'
    author = factory.SubFactory(UserF)
    version = factory.SubFactory('changes.tests.model_factories.VersionF')
    category = factory.SubFactory('changes.tests.model_factories.CategoryF')


class VersionF(factory.django.DjangoModelFactory):
    """
    Version model factory
    """
    class Meta:
        model = Version

    padded_version = factory.Sequence(lambda n: u'100001100 %s' % n)
    image_file = factory.django.ImageField(color='green')
    author = factory.SubFactory(UserF)
    description = u'This description is really only here for testing'
    project = factory.SubFactory('base.tests.model_factories.ProjectF')


class SponsorF(factory.django.DjangoModelFactory):
    """
    Sponsors model factory
    """
    class Meta:
        model = Sponsor

    name = factory.Sequence(lambda n: u'Test Sponsor Name %s' % n)
    address = factory.Sequence(lambda n: u'Address\nline2\n%s' % n)
    country = 'za'
    sponsor_url = factory.Sequence(lambda n: u'Test URL %s' % n)
    contact_person = factory.Sequence(lambda n: u'Test Contact Person %s' % n)
    sponsor_email = factory.Sequence(lambda n: u'Test Sponsor Email %s' % n)
    approved = True
    author = factory.SubFactory(UserF)
    logo = factory.django.ImageField(color='green')
    agreement = factory.django.ImageField(color='green')
    project = factory.SubFactory('base.tests.model_factories.ProjectF')


class SponsorshipLevelF(factory.django.DjangoModelFactory):
    """
    Sponsorship Level model factory
    """
    class Meta:
        model = SponsorshipLevel

    name = factory.Sequence(lambda n: u'Test Sponsorship level %s' % n)
    currency = factory.Sequence(lambda n: u'Test Currency %s' % n)
    approved = True
    author = factory.SubFactory(UserF)
    value = factory.Sequence(lambda n: n)
    logo = factory.django.ImageField(color='green')
    project = factory.SubFactory('base.tests.model_factories.ProjectF')


class SponsorshipPeriodF(factory.django.DjangoModelFactory):
    """
    Sponsorship Period model factory
    """
    class Meta:
        model = SponsorshipPeriod

    start_date = factory.fuzzy.FuzzyDate(date(2014, 1, 1))
    end_date = factory.fuzzy.FuzzyDate(
        start_date=datetime.date(datetime.now()) + timedelta(days=365),
        end_date=datetime.date(datetime.now()) + timedelta(days=750),
    )
    approved = True
    author = factory.SubFactory(UserF)
    project = factory.SubFactory('base.tests.model_factories.ProjectF')
    sponsor = factory.SubFactory('changes.tests.model_factories.SponsorF')
    sponsorship_level = factory.SubFactory(
            'changes.tests.model_factories.SponsorshipLevelF')
