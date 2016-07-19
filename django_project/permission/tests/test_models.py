# coding=utf-8
"""Tests for models."""
from base.tests.model_factories import ProjectF
from core.model_factories import UserF
from django.test import TestCase
from permission.tests.model_factories import ProjectAdministratorF, ProjectCollaboratorF


class TestProjectAdministrator(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Project_Administrator_create(self):
        """
        Tests Category model creation
        """
        model = ProjectAdministratorF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_Project_Administrator_read(self):
        """
        Tests Category model read
        """
        project = ProjectF.create(
            name='Custom Project',
            slug='custom-project'
        )
        user = UserF.create(**{
            'username': 'irwan',
            'password': 'password',
            'is_staff': False
        })
        model = ProjectAdministratorF.create(
            project=project,
            user=user
        )

        self.assertTrue(model.project.name == 'Custom Project')
        self.assertTrue(model.project.slug == 'custom-project')
        self.assertTrue(model.user.username == 'irwan')

    def test_Project_Administrator_update(self):
        """
        Tests Category model update
        """
        model = ProjectAdministratorF.create()
        project = ProjectF.create(
            name='new project',
            slug='new-project'
        )
        user = UserF.create(**{
            'username': 'irwan update',
            'password': 'password',
            'is_staff': False
        })
        model.project = project
        model.user = user
        model.save()

        # check if updated
        self.assertEqual(model.project, project)
        self.assertEqual(model.user, user)

    def test_Project_Administrator_delete(self):
        """
        Tests Category model delete
        """
        model = ProjectAdministratorF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)


class TestProjectCollaborator(TestCase):
    """
    Tests search models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Project_Collaborator_create(self):
        """
        Tests Category model creation
        """
        model = ProjectCollaboratorF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_Project_Collaborator_read(self):
        """
        Tests Category model read
        """
        project = ProjectF.create(
            name='Custom Project',
            slug='custom-project'
        )
        user = UserF.create(**{
            'username': 'irwan',
            'password': 'password',
            'is_staff': False
        })
        model = ProjectCollaboratorF.create(
            project=project,
            user=user
        )

        self.assertTrue(model.project.name == 'Custom Project')
        self.assertTrue(model.project.slug == 'custom-project')
        self.assertTrue(model.user.username == 'irwan')

    def test_Project_Collaborator_update(self):
        """
        Tests Category model update
        """
        model = ProjectCollaboratorF.create()
        project = ProjectF.create(
            name='new project',
            slug='new-project'
        )
        user = UserF.create(**{
            'username': 'irwan update',
            'password': 'password',
            'is_staff': False
        })
        model.project = project
        model.user = user
        model.save()

        # check if updated
        self.assertEqual(model.project, project)
        self.assertEqual(model.user, user)

    def test_Project_Collaborator_delete(self):
        """
        Tests Category model delete
        """
        model = ProjectCollaboratorF.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)
