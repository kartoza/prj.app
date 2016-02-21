# coding=utf-8
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
        model = ProjectF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if name exists
        self.assertTrue(model.name is not None)

    def test_Project_read(self):
        """
        Tests Project model read
        """
        model = ProjectF.create(
            name='Custom Project',
            slug='custom-project'
        )

        self.assertTrue(model.name == 'Custom Project')
        self.assertTrue(model.slug == 'custom-project')

    def test_Project_update(self):
        """
        Tests Project model update
        """
        model = ProjectF.create()
        new_model_data = {
            'name': u'New Project Name',
            'description': u'New description',
            'approved': False,
            'private': True,
            'slug': u'new-project-slug'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Project_delete(self):
        """
        Tests Project model delete
        """
        model = ProjectF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)
