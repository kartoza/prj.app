# noinspection PyUnresolvedReferences,PyPackageRequirements
import factory
from base.models.project import Project
from core.model_factories import UserF


class ProjectF(factory.django.DjangoModelFactory):
    """
    Project model factory
    """
    #FACTORY_FOR = Project
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: 'Test Project %s' % n)
    description = u'This is only for testing'
    owner = factory.SubFactory(UserF)
    approved = True
    private = False
