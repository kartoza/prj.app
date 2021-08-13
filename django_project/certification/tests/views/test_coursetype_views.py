from django.test import TestCase, override_settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from certification.tests.model_factories import (
    CourseTypeF, CertifyingOrganisationF, ProjectF)


@override_settings(VALID_DOMAIN=['testserver', ])
class TestCourseTypeView(TestCase):
    """Test the CourseType views."""

    def setUp(self):
        self.client.post(
            '/set_language/', data={'language': 'en'})
        self.project = ProjectF.create()
        self.certifying_organisation = CertifyingOrganisationF.create(
            project=self.project
        )
        self.coursetype = CourseTypeF.create(
            name="test",
            certifying_organisation=self.certifying_organisation
        )

    def test_CourseType_url_patterns(self):
        """Test the valid url patterns."""

        url = reverse('coursetype-detail', kwargs={
            'project_slug': self.project.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'pk': self.coursetype.pk
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # When user are trying to use the old pattern,
        # it should raise NoReverseMatch
        with self.assertRaises(NoReverseMatch):
            reverse('coursetype-detail', kwargs={
                'project_slug': self.project.slug,
                'organisation_slug': self.certifying_organisation.slug,
                'pk': self.coursetype.slug
            })
