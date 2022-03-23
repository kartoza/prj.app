from bs4 import BeautifulSoup as Soup
from django.shortcuts import reverse
from django.test import TestCase, override_settings

from base.tests.model_factories import ProjectF
from core.model_factories import UserF
from certification.tests.model_factories import (
    CertificateTypeF,
    ProjectCertificateTypeF
)


class TestCertificateTypesView(TestCase):

    def setUp(self):
        self.project = ProjectF.create()
        another_project = ProjectF.create()
        self.certificate_type_1 = CertificateTypeF.create(name='type-1')
        self.certificate_type_2 = CertificateTypeF.create(name='type-2')
        ProjectCertificateTypeF.create(
            project=self.project, certificate_type=self.certificate_type_1
        )
        ProjectCertificateTypeF.create(
            project=another_project, certificate_type=self.certificate_type_2
        )
        self.user = UserF.create(**{
            'username': 'tester',
            'password': 'password',
            'is_staff': False,
        })

        self.user_manager = UserF.create(**{
            'username': 'manager',
            'password': 'password',
            'is_staff': False,
        })
        self.project.certification_managers.add(self.user_manager)

        self.user_staff = UserF.create(**{
            'username': 'staff',
            'password': 'password',
            'is_staff': True,
        })

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_certificate_type_view_contains_course_type(self):
        """Test CertificateType list page."""

        self.client.post('/set_language/', data={'language': 'en'})
        self.client.force_login(self.user_staff)
        url = reverse('certification-management-view', kwargs={
            'project_slug': self.project.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # all certificate types should be displayed
        self.assertContains(response, self.certificate_type_1.name)
        self.assertContains(response, self.certificate_type_2.name)

        # only certificate types related to project in context_object ListView
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(
            response.context_data['object_list'].last().certificate_type,
            self.certificate_type_1
        )

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_certificate_type_user_is_manager(self):
        self.client.post('/set_language/', data={'language': 'en'})
        self.client.force_login(self.user_manager)
        url = reverse('certification-management-view', kwargs={
            'project_slug': self.project.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_certificate_type_non_manager_should_return404(self):
        self.client.post('/set_language/', data={'language': 'en'})
        self.client.force_login(self.user)
        url = reverse('certification-management-view', kwargs={
            'project_slug': self.project.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_project_certificate_view(self):
        self.client.post('/set_language/', data={'language': 'en'})
        self.client.force_login(self.user_staff)
        url = reverse('certificate-type-update', kwargs={
            'project_slug': self.project.slug
        })
        # choose certificate type-2 only
        post_data = {'certificate_types': 'type-2'}
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        soup = Soup(response.content, "html5lib")
        self.assertTrue(len(soup.find_all('input', checked=True)) == 1)
        self.assertEqual(soup.find('input', checked=True)["value"], "type-2")

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_project_certificate_view_user_is_manager(self):
        self.client.post('/set_language/', data={'language': 'en'})
        self.client.force_login(self.user_manager)
        url = reverse('certificate-type-update', kwargs={
            'project_slug': self.project.slug
        })
        # choose certificate type-2 only
        post_data = {'certificate_types': 'type-2'}
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)

    @override_settings(VALID_DOMAIN=['testserver', ])
    def test_update_project_certificate_non_manager_should_return404(self):
        self.client.post('/set_language/', data={'language': 'en'})
        self.client.force_login(self.user)
        url = reverse('certificate-type-update', kwargs={
            'project_slug': self.project.slug
        })
        # choose certificate type-2 only
        post_data = {'certificate_types': 'type-2'}
        response = self.client.post(url, data=post_data, follow=True)
        self.assertRedirects(
            response,
            expected_url=reverse(
                'certification-management-view',
                kwargs={'project_slug': self.project.slug}
            ),
            status_code=302,
            target_status_code=404
        )
