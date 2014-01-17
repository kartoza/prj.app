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
        my_model = ProjectF.create()

        #check if PK exists
        self.assertTrue(my_model.pk is not None)

        #check if name exists
        self.assertTrue(my_model.name is not None)

    def test_Project_read(self):
        """
        Tests Project model read
        """
        my_model = ProjectF.create(
            name='Custom Project',
            slug='custom-project'
        )

        self.assertTrue(my_model.name == 'Custom Project')
        self.assertTrue(my_model.slug == 'custom-project')

    def test_Project_update(self):
        """
        Tests Project model update
        """
        my_model = ProjectF.create()
        new_model_data = {
            'name': u'New Project Name',
            'description': u'New description',
            'approved': False,
            'private': True,
            'slug': u'new-project-slug'
        }
        my_model.__dict__.update(new_model_data)
        my_model.save()

        #check if updated
        for key, val in new_model_data.items():
            self.assertEqual(my_model.__dict__.get(key), val)

    def test_Project_delete(self):
        """
        Tests Project model delete
        """
        my_model = ProjectF.create()

        my_model.delete()

        #check if deleted
        self.assertTrue(my_model.pk is None)
