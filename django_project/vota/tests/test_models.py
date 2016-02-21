from django.test import TestCase
from vota.tests.model_factories import BallotF, VoteF, CommitteeF


class TestBallotCRUD(TestCase):
    """Tests search models."""

    def setUp(self):
        """Sets up before each test."""
        pass

    def test_ballot_create(self):
        """Tests Ballot model creation."""
        model = BallotF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_ballot_read(self):
        """Tests Ballot model read."""
        model = BallotF.create(
            name=u'Custom Ballot'
        )

        self.assertTrue(model.name == 'Custom Ballot')
        self.assertTrue(model.slug == 'custom-ballot')

    def test_ballot_update(self):
        """Tests Ballot model update."""
        model = BallotF.create()
        new_model_data = {
            'name': u'New Ballot Name',
            'summary': u'New summary',
            'description': u'This is a great description',
            'approved': False,
            'no_quorum': True,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_ballot_delete(self):
        """
        Tests Ballot model delete
        """
        model = BallotF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestVoteCRUD(TestCase):
    """Tests search models."""

    def setUp(self):
        """Sets up before each test."""
        pass

    def test_vote_create(self):
        """Tests Vote model creation."""
        model = VoteF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if we have a user
        self.assertTrue(model.user is not None)

    def test_vote_read(self):
        """Tests Vote model read."""
        model = VoteF.create(choice='n')

        self.assertTrue(model.choice == 'n')

    def test_vote_update(self):
        """Tests Vote model update."""
        model = VoteF.create()
        new_model_data = {
            'choice': 'y'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_vote_delete(self):
        """Tests Vote model delete."""
        model = VoteF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestCommitteeCRUD(TestCase):
    """Tests search models."""

    def setUp(self):
        """Sets up before each test."""
        pass

    def test_committee_create(self):
        """Tests Committee model creation."""
        model = CommitteeF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_committee_read(self):
        """Tests Committee model read."""
        model = CommitteeF.create(
            name=u'Custom Committee'
        )

        self.assertTrue(model.name == 'Custom Committee')
        self.assertTrue(model.slug == 'custom-committee')

    def test_committee_update(self):
        """Tests Committee model update."""
        model = CommitteeF.create()
        new_model_data = {
            'name': u'New Committee Name',
            'description': u'New description',
            'quorum_setting': u'50'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_committee_delete(self):
        """Tests Committee model delete."""
        model = CommitteeF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)
