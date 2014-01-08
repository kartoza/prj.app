import factory
import datetime
from vota.models.ballot import Ballot
from vota.models.committee import Committee
from vota.models.vote import Vote


class BallotF(factory.DjangoModelFactory):
    """
    Ballot model factory
    """
    FACTORY_FOR = Ballot

    name = factory.Sequence(lambda n: u'Test Ballot %s' % n)
    summary = u'This summary is excellent.'
    description = u'This description is equally wonderful'
    approved = True
    denied = False
    no_quorum = False
    open_from = datetime.datetime.now() - datetime.timedelta(days=7)
    closes = datetime.datetime.now() + datetime.timedelta(days=7)
    private = False
    committee = factory.SubFactory('vota.tests.model_factories.CommitteeF')


class CommitteeF(factory.DjangoModelFactory):
    """
    Committee model factory
    """
    FACTORY_FOR = Committee

    name = factory.Sequence(lambda n: u'Test Committee %s' % n)
    description = u'This description is really only here for testing'
    sort_number = 1
    quorum_setting = u'100'
    project = factory.SubFactory('base.tests.model_factories.ProjectF')

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of users were passed in, use them
            for user in extracted:
                self.users.add(user)


class VoteF(factory.DjangoModelFactory):
    """
    Vote model factory
    """
    FACTORY_FOR = Vote

    positive = True
    abstain = False
    negative = False
    user = factory.SubFactory('core.model_factories.UserF')
    ballot = factory.SubFactory('vota.tests.model_factories.BallotF')
