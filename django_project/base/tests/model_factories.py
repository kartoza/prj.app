import factory
from base.models.project import Project


class ProjectF(factory.django.DjangoModelFactory):
    """
    Project model factory
    """
    FACTORY_FOR = Project

    name = factory.Sequence(lambda n: 'Test Project %s' % n)
    description = u'This is only for testing'
    approved = True
    private = False
