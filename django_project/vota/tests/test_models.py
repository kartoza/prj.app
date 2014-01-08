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
        myModel = BallotF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

        #check if name exists
        self.assertTrue(myModel.name is not None)

    def test_Ballot_read(self):
        """
        Tests Ballot model read
        """
        myModel = BallotF.create(
            name=u'Custom Ballot'
        )

        self.assertTrue(myModel.name == 'Custom Ballot')
        self.assertTrue(myModel.slug == 'custom-ballot')

    def test_Ballot_update(self):
        """
        Tests Ballot model update
        """
        myModel = BallotF.create()
        myNewModelData = {
            'name': u'New Ballot Name',
            'summary': u'New summary',
            'description': u'This is a great description',
            'approved': False,
            'no_quorum': True,
        }
        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_Ballot_delete(self):
        """
        Tests Ballot model delete
        """
        myModel = BallotF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)


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
        myModel = VoteF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

        #check if we have a user
        self.assertTrue(myModel.user is not None)

    def test_Vote_read(self):
        """
        Tests Vote model read
        """
        myModel = VoteF.create(choice='n')

        self.assertTrue(myModel.choice == 'n')

    def test_Vote_update(self):
        """
        Tests Vote model update
        """
        myModel = VoteF.create()
        myNewModelData = {
            'choice': 'y'
        }
        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_Vote_delete(self):
        """
        Tests Vote model delete
        """
        myModel = VoteF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)


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
        myModel = CommitteeF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

        #check if name exists
        self.assertTrue(myModel.name is not None)

    def test_Committee_read(self):
        """
        Tests Committee model read
        """
        myModel = CommitteeF.create(
            name=u'Custom Committee'
        )

        self.assertTrue(myModel.name == 'Custom Committee')
        self.assertTrue(myModel.slug == 'custom-committee')

    def test_Committee_update(self):
        """
        Tests Committee model update
        """
        myModel = CommitteeF.create()
        myNewModelData = {
            'name': u'New Committee Name',
            'description': u'New description',
            'quorum_setting': u'50'
        }
        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_Committee_delete(self):
        """
        Tests Committee model delete
        """
        myModel = CommitteeF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)
