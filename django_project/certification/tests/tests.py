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


class TestAttendee(TestCase):
    """
    Test attendee model.
    """
    def setUp(self):
        """
        Set up before test.
        """
        pass

  #  def test_Attendee_create(self):
        """
        Test certificate model creation.
        """
 #       model = AttendeeF.create()

        # check if PK exists
        #self.assertTrue(model.pk is not None)

        # check if model name exists
#        self.assertTrue(model.name is not None)


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
        Test certificate model creation.
        """
        model = CourseF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if model name exists
        self.assertTrue(model.name is not None)


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
        Test certificate model creation.
        """
        model = TrainingCenterF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)

        # check if model name exists
        self.assertTrue(model.name is not None)

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
        Test certificate model creation.
        """
        model = CourseTypeF.create()

        # check if PK exists
        self.assertTrue(model.pk is not None)
