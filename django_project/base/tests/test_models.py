from django.test import TestCase
from base.tests.model_factories import ProjectF


class TestProjectCRUD(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Project_create(self):
        """
        Tests Project model creation
        """
        myModel = ProjectF.create()

        #check if PK exists
        self.assertTrue(myModel.pk is not None)

        #check if name exists
        self.assertTrue(myModel.name is not None)

    def test_Project_read(self):
        """
        Tests Project model read
        """
        myModel = ProjectF.create(
            name='Custom Project',
            slug='custom-project'
        )

        self.assertTrue(myModel.name == 'Custom Project')
        self.assertTrue(myModel.slug == 'custom-project')

    def test_Project_update(self):
        """
        Tests Project model update
        """
        myModel = ProjectF.create()
        myNewModelData = {
            'name': u'New Project Name',
            'description': u'New description',
            'approved': False,
            'private': True,
            'slug': u'new-project-slug'
        }
        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(myModel.__dict__.get(key), val)

    def test_Project_delete(self):
        """
        Tests Project model delete
        """
        myModel = ProjectF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)
