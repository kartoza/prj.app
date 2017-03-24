# coding=utf-8
"""Test for models."""

from django.test import TestCase
from certification.tests.model_factories import (
    CertificateF,
    AttendeeF,
    CourseF,
    CourseTypeF,
    CourseConvenerF,
    CertifyingOrganisationF,
    TrainingCenterF)


class TestCertifyingOrganisation(TestCase):
    """
    Test certifying organisation model.
    """
    def setUp(self):
        """
        Set up before each test.
        """
        pass

    def test_Certifying_Organisation_create(self):
        """
        Test certifying organisation model creation.
        """
        model = CertifyingOrganisationF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if model name exists
        self.assertTrue(model.name is not None)

    def test_Certifying_Organisation_delete(self):
        """
        Test course type model creation.
        """
        model = CertifyingOrganisationF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_Certifying_Organisation_read(self):
        """
        Test certifying organisation model read.
        """
        model = CertifyingOrganisationF.create(
            name=u'Certifying Organisation update'
        )

        self.assertTrue(model.name == 'Certifying Organisation update')

    def test_Certifying_Organisation_update(self):
        """
        Test certifying organisation update.
        """
        model = CertifyingOrganisationF.create()
        new_model_data = {
            'name': u'new organisation name',
            'organisation_email': u'new organisation email',
            'organisation_phone': u'new organisation phone',
            'approved': False,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)


class TestCertificate(TestCase):
    """
    Test certificate model.
    """
    def setUp(self):
        """
        Set up before test.
        """
        pass

    def test_Certificate_create(self):
        """
        Test certificate model creation.
        """
        model = CertificateF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_Certificate_delete(self):
        """
        Test certificate model deletion.
        """
        model = CertificateF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_Certificate_update(self):
        """
        Test attendee model update
        """
        model = CertificateF.create()
        new_model_data = {
            'id_id': 'new ID certificate name',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)


class TestAttendee(TestCase):
    """
    Test attendee model.
    """
    def setUp(self):
        """
        Set up before test.
        """
        pass

    def test_Attendee_create(self):
        """
        Test attendee model creation.
        """
        model = AttendeeF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if model variable exists
        self.assertTrue(model.firstname is not None)

    def test_Attendee_delete(self):
        """
        Test attendee model deletion.
        """
        model = AttendeeF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_Attendee_update(self):
        """
        Test attendee model update
        """
        model = AttendeeF.create()
        new_model_data = {
            'firstname': 'new attendee firstname',
            'surname': 'new attendee surname',
            'email': 'new attendee email'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)


class TestCourse(TestCase):
    """
    Test course model.
    """
    def setUp(self):
        """
        Set up before test.
        """
        pass

    def test_Course_create(self):
        """
        Test course model creation.
        """
        model = CourseF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if model name exists
        self.assertTrue(model.name is not None)

    def test_Course_delete(self):
        """
        Test course model deletion.
        """
        model = CourseF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_Course_update(self):
        """
        Test attendee model update
        """
        model = CourseF.create()
        new_model_data = {
            'name': 'new course name',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)


class TestTrainingCenter(TestCase):
    """
    Test training center model.
    """
    def setUp(self):
        """
        Set up before test.
        """
        pass

    def test_Training_Center_create(self):
        """
        Test training center model creation.
        """
        model = TrainingCenterF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if model name exists
        self.assertTrue(model.name is not None)
        self.assertTrue(model.phone is not None)
        self.assertTrue(model.Address is not None)
        self.assertTrue(model.email is not None)

    def test_Training_Center_delete(self):
        """
        Test training center model deletion.
        """
        model = TrainingCenterF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_Training_Center_update(self):
        """
        Test attendee model update
        """
        model = TrainingCenterF.create()
        new_model_data = {
            'name': 'new Training Center name',
            'email': 'new Training Center email',
            'phone': 'new Training Center phone',
            'Address': 'new Training Center address',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)
        self.assertTrue(model.Address == 'new Training Center address')


class TestCourseType(TestCase):
    """
    Test certificate model.
    """
    def setUp(self):
        """
        Set up before test.
        """
        pass

    def test_Course_Type_create(self):
        """
        Test course type model creation.
        """
        model = CourseTypeF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_Course_Type_delete(self):
        """
        Test course type model deletion.
        """
        model = CourseTypeF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)

    def test_Course_Type_update(self):
        """
        Test attendee model update
        """
        model = CourseTypeF.create()
        new_model_data = {
            'name': 'new Course Type name',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)


class TestCourseConvener(TestCase):
    """
    Test course convener model.
    """
    def setUp(self):
        """
        Set up before test.
        """
        pass

    def test_Course_Convener_create(self):
        """
        Test course convener model creation.
        """
        model = CourseConvenerF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

    def test_Course_Convener_delete(self):
        """
        Test course convener model delete.
        """
        model = CourseConvenerF.create()
        model.delete()

        # check if deleted
        self.assertTrue(model.pk is None)
