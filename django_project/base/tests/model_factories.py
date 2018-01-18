# noinspection PyUnresolvedReferences,PyPackageRequirements
import factory
from base.models import Project, Organisation
from core.model_factories import UserF


class ProjectF(factory.django.DjangoModelFactory):
    """
    Project model factory
    """
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: 'Test Project %s' % n)
    description = u'This is only for testing'
    owner = factory.SubFactory(UserF)
    approved = True
    private = False
    gitter_room = u'test/test'


class OrganisationF(factory.django.DjangoModelFactory):
    """
    Organisation model factory
    """
    class Meta:
        model = Organisation

    name = 'Test Organisation'
    owner = factory.SubFactory(UserF)
    approved = True
