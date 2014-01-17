# noinspection PyUnresolvedReferences,PyPackageRequirements
import factory
from changes.models.category import Category
from changes.models.entry import Entry
from changes.models.version import Version
from core.model_factories import UserF


class CategoryF(factory.django.DjangoModelFactory):
    """
    Category model factory
    """
    FACTORY_FOR = Category

    name = factory.Sequence(lambda n: u'Test Category %s' % n)
    approved = True
    sort_number = factory.Sequence(lambda n: n)
    project = factory.SubFactory('base.tests.model_factories.ProjectF')


class EntryF(factory.django.DjangoModelFactory):
    """
    Entry model factory
    """
    FACTORY_FOR = Entry

    title = factory.Sequence(lambda n: u'This is a great title: %s' % n)
    description = u'This description is really only here for testing'
    image_file = factory.django.ImageField(color='blue')
    image_credits = u'The credits go to dodobas'
    author = factory.SubFactory(UserF)
    approved = True
    version = factory.SubFactory('changes.tests.model_factories.VersionF')
    category = factory.SubFactory('changes.tests.model_factories.CategoryF')


class VersionF(factory.django.DjangoModelFactory):
    """
    Version model factory
    """
    FACTORY_FOR = Version

    name = factory.Sequence(lambda n: u'Version 1.0.%s' % n)
    approved = True
    image_file = factory.django.ImageField(color='green')
    author = factory.SubFactory(UserF)
    description = u'This description is really only here for testing'
    project = factory.SubFactory('base.tests.model_factories.ProjectF')
