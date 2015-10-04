from django.test import TestCase
from vota.tests.model_factories import BallotF, VoteF, CommitteeF


class TestBallotCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Ballot_create(self):
        """
        Tests Ballot model creation
        """
        my_model = BallotF.create()

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if name exists
        self.assertTrue(my_model.name is not None)

    def test_Ballot_read(self):
        """
        Tests Ballot model read
        """
        my_model = BallotF.create(
            name=u'Custom Ballot'
        )

        self.assertTrue(my_model.name == 'Custom Ballot')
        self.assertTrue(my_model.slug == 'custom-ballot')

    def test_Ballot_update(self):
        """
        Tests Ballot model update
        """
        my_model = BallotF.create()
        new_model_data = {
            'name': u'New Ballot Name',
            'summary': u'New summary',
            'description': u'This is a great description',
            'approved': False,
            'no_quorum': True,
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Ballot_delete(self):
        """
        Tests Ballot model delete
        """
        my_model = BallotF.create()

        my_model.delete()

        # check if deleted
        self.assertTrue(my_model.pk is None)


class TestVoteCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Vote_create(self):
        """
        Tests Vote model creation
        """
        my_model = VoteF.create()

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if we have a user
        self.assertTrue(my_model.user is not None)

    def test_Vote_read(self):
        """
        Tests Vote model read
        """
        my_model = VoteF.create(choice='n')

        self.assertTrue(my_model.choice == 'n')

    def test_Vote_update(self):
        """
        Tests Vote model update
        """
        my_model = VoteF.create()
        new_model_data = {
            'choice': 'y'
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Vote_delete(self):
        """
        Tests Vote model delete
        """
        my_model = VoteF.create()

        my_model.delete()

        # check if deleted
        self.assertTrue(my_model.pk is None)


class TestCommitteeCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Committee_create(self):
        """
        Tests Committee model creation
        """
        my_model = CommitteeF.create()

        # check if PK exists
        self.assertTrue(my_model.pk is not None)

        # check if name exists
        self.assertTrue(my_model.name is not None)

    def test_Committee_read(self):
        """
        Tests Committee model read
        """
        my_model = CommitteeF.create(
            name=u'Custom Committee'
        )

        self.assertTrue(my_model.name == 'Custom Committee')
        self.assertTrue(my_model.slug == 'custom-committee')

    def test_Committee_update(self):
        """
        Tests Committee model update
        """
        my_model = CommitteeF.create()
        new_model_data = {
            'name': u'New Committee Name',
            'description': u'New description',
            'quorum_setting': u'50'
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Committee_delete(self):
        """
        Tests Committee model delete
        """
        my_model = CommitteeF.create()

        my_model.delete()

        # check if deleted
        self.assertTrue(my_model.pk is None)
