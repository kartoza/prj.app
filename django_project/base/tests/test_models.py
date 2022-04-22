# coding=utf-8
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from base.tests.model_factories import ProjectF
from django.core.exceptions import ValidationError
from base.models.project import Project
from changes.tests.model_factories import VersionF


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

        self.assertTrue(
            model.external_reviewer_invitation is not None)

    @override_settings(PROJECT_VERSION_LIST_SIZE=2)
    def test_Project_read(self):
        """
        Tests Project model read
        """
        model = ProjectF.create(
            name='Custom Project',
            slug='custom-project',
            external_reviewer_invitation='test',
            approved=True
        )
        version2 = VersionF.create(
            name='version_2',
            project=model,
            padded_version='2'
        )
        version = VersionF.create(
            name='version_1',
            project=model,
            padded_version='1'
        )

        self.assertTrue(model.name == 'Custom Project')
        self.assertTrue(model.slug == 'custom-project')
        self.assertEqual(
            'test',
            model.external_reviewer_invitation)
        self.assertTrue(
            str(model),
            model.name
        )
        self.assertTrue(
            model.get_absolute_url(),
            reverse('project-detail', kwargs={'slug': model.slug})
        )
        self.assertIn(
            version,
            model.versions()
        )
        self.assertIn(
            version2,
            model.latest_versions()
        )
        self.assertEqual(
            model.pagination_threshold(),
            2
        )
        self.assertTrue(
            model.pagination_threshold_exceeded()
        )
        version.delete()
        self.assertFalse(
            model.pagination_threshold_exceeded()
        )
        self.assertNotIn(
            model,
            Project.unapproved_objects.all()
        )

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
            'project_url': u'http://foo.org',
            'slug': u'new-project-slug',
            'gitter_room': u'test/new',
            'is_lessons': True,
            'is_sustaining_members': True,
            'is_teams': True,
            'is_changelogs': True,
            'is_certification': True
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

    def test_gitter_validation(self):
        """
        Test validation for gitter room field
        """
        model = ProjectF.create()

        new_model_data = {
            'name': u'New Project Name',
            'description': u'New description',
            'approved': False,
            'private': True,
            'project_url': u'http://foo.org',
            'slug': u'new-project-slug',
            'gitter_room': u'invalid',
        }

        model.__dict__.update(new_model_data)
        with self.assertRaises(ValidationError):
            if model.full_clean():
                model.save()

        self.assertEqual(
            Project.objects.filter(gitter_room='invalid').count(), 0)

    def test_unidecode(self):
        """
        Tests unidecode() to represent special characters into ASCII
        """
        model = ProjectF.create(name=u'straße',)

        # check if properly decoded into ASCII
        self.assertTrue(model.slug == "strasse")
