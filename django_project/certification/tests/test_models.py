# coding=utf-8
"""Test for models."""

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from certification.tests.model_factories import (
    CertificateF,
    CertificateTypeF,
    AttendeeF,
    CourseF,
    CourseTypeF,
    CourseConvenerF,
    CertifyingOrganisationF,
    TrainingCenterF,
    CourseAttendeeF,
    StatusF, ExternalReviewerF, ChecklistF
)
from certification.models.certificate_type import CertificateType
from core.model_factories import UserF


class SetUpMixin:
    def setUp(self):
        """Set up before each test."""
        # Delete CertificateType created from migration 0007_certificate_type
        CertificateType.objects.all().delete()


class TestCertifyingOrganisation(TestCase):
    """Test certifying organisation model."""

    def setUp(self):
        """Set up before each test."""

        pass

    def test_Certifying_Organisation_create(self):
        """Test certifying organisation model creation."""

        model = CertifyingOrganisationF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model attributes exists.
        self.assertTrue(model.name is not None)
        self.assertTrue(model.organisation_email is not None)
        self.assertTrue(model.address is not None)
        self.assertTrue(model.organisation_phone is not None)
        self.assertTrue(model.approved is not None)
        self.assertTrue(model.project is not None)
        self.assertTrue(model.creation_date is not None)
        self.assertTrue(model.update_date is not None)

    def test_Certifying_Organisation_delete(self):
        """Test course type model creation."""

        model = CertifyingOrganisationF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)

    def test_Certifying_Organisation_read(self):
        """Test certifying organisation model read."""

        model = CertifyingOrganisationF.create(
            name=u'Certifying Organisation update',
            organisation_email=u'CertifyingOrganisation@gmail.com',
            address=u'Certifying Org address 123',
            organisation_phone=u'+260972394874',
            approved=u'True',
        )

        self.assertTrue(
            model.name == 'Certifying Organisation update'
        )
        self.assertTrue(
            model.organisation_email == 'CertifyingOrganisation@gmail.com'
        )
        self.assertTrue(
            model.address == 'Certifying Org address 123'
        )
        self.assertTrue(
            model.organisation_phone == '+260972394874'
        )
        self.assertTrue(
            model.approved == 'True'
        )

    def test_Certifying_Organisation_update(self):
        """Test certifying organisation update."""

        model = CertifyingOrganisationF.create()
        new_model_data = {
            'name': u'new organisation name',
            'organisation_email': u'new organisation email',
            'organisation_phone': u'new organisation phone',
            'address': u'new address',
            'approved': False,
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)


class CertificateSetUp(SetUpMixin, TestCase):
    """Test certificate model."""

    def test_Certificate_create(self):
        """Test certificate model creation."""
        model = CertificateF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

    def test_Certificate_delete(self):
        """Test certificate model deletion."""

        model = CertificateF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)



class CertificateTypeSetUp(SetUpMixin, TestCase):
    """Test Certificate models."""

    def test_CRUD_CertificateType(self):
        # initial
        self.assertEqual(CertificateType.objects.all().count(), 0)

        # create model
        model = CertificateTypeF.create()
        self.assertEqual(CertificateType.objects.all().count(), 1)

        # read model
        self.assertIsNotNone(model.id)
        self.assertIn('Test certificate type name', model.name)
        self.assertIn('Description certificate type', model.description)
        self.assertIn('Wording certificate type', model.wording)
        self.assertEqual(model.__str__(), model.name)

        #
        model.name = 'Update certificate type  name'
        model.save()
        self.assertEqual(model.name, 'Update certificate type  name')

        model.delete()
        self.assertIsNone(model.id)
        self.assertEqual(CertificateType.objects.all().count(), 0)

    def test_name_field_must_be_unique(self):
        CertificateTypeF.create(name="We are twin")
        msg = ('duplicate key value violates unique constraint '
               '"certification_certificatetype_name_key"')
        with self.assertRaisesMessage(IntegrityError, msg):
            CertificateTypeF.create(name="We are twin")

    def test_order_field_must_be_unique(self):
        CertificateTypeF.create(order=1)
        msg = ('duplicate key value violates unique constraint '
               '"certification_certificatetype_order_key"')
        with self.assertRaisesMessage(IntegrityError, msg):
            CertificateTypeF.create(order=1)

    def test_order_field_can_be_null(self):
        model_1 = CertificateTypeF.create(order=1)
        model_2 = CertificateTypeF.create(order=2)

        self.assertEqual(model_1.order, 1)
        self.assertEqual(model_2.order, 2)

        model_1.order = None
        model_1.save()

        model_2.order = 1
        model_2.save()

        self.assertEqual(model_1.order, None)
        self.assertEqual(model_2.order, 1)


class TestAttendee(TestCase):
    """Test attendee model."""

    def setUp(self):
        """Set up before test."""

        pass

    def test_Attendee_create(self):
        """Test attendee model creation."""

        model = AttendeeF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model variable exists.
        self.assertTrue(model.firstname is not None)
        self.assertTrue(model.surname is not None)
        self.assertTrue(model.email is not None)
        self.assertTrue(model.slug is not None)
        self.assertTrue(model.certifying_organisation is not None)
        self.assertTrue(model.author is not None)

    def test_Attendee_delete(self):
        """Test attendee model deletion."""

        model = AttendeeF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)

    def test_Attendee_update(self):
        """Test attendee model update."""

        model = AttendeeF.create()
        new_model_data = {
            'firstname': 'new attendee firstname',
            'surname': 'new attendee surname',
            'email': 'new attendee email',
            'slug': 'new-attendee-slug'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)


class TestCourse(TestCase):
    """Test course model."""

    def setUp(self):
        """Set up before test."""

        pass

    def test_Course_create(self):
        """Test course model creation."""

        model = CourseF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model attributes exists.
        self.assertTrue(model.name is not None)
        self.assertTrue(model.language is not None)
        self.assertTrue(model.course_convener is not None)
        self.assertTrue(model.certifying_organisation is not None)
        self.assertTrue(model.course_type is not None)
        self.assertTrue(model.training_center is not None)
        self.assertTrue(model.author is not None)

    def test_Course_delete(self):
        """Test course model deletion."""

        model = CourseF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)


class TestTrainingCenter(TestCase):
    """Test training center model."""

    def setUp(self):
        """Set up before test."""

        pass

    def test_Training_Center_create(self):
        """Test training center model creation."""

        model = TrainingCenterF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model name exists.
        self.assertTrue(model.name is not None)
        self.assertTrue(model.phone is not None)
        self.assertTrue(model.address is not None)
        self.assertTrue(model.email is not None)

    def test_Training_Center_delete(self):
        """Test training center model deletion."""

        model = TrainingCenterF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)

    def test_Training_Center_update(self):
        """Test attendee model update."""

        model = TrainingCenterF.create()
        new_model_data = {
            'name': 'new Training Center name',
            'email': 'new Training Center email',
            'phone': 'new Training Center phone',
            'Address': 'new Training Center address',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)
            self.assertTrue(model.Address == 'new Training Center address')
            self.assertTrue(model.phone == 'new Training Center phone')
            self.assertTrue(model.email == 'new Training Center email')
            self.assertTrue(model.name == 'new Training Center name')


class TestCourseType(TestCase):
    """Test course type model."""

    def setUp(self):
        """Set up before test."""

        pass

    def test_Course_Type_create(self):
        """Test course type model creation."""

        model = CourseTypeF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

    def test_Course_Type_delete(self):
        """Test course type model deletion."""

        model = CourseTypeF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)

    def test_Course_Type_update(self):
        """Test attendee model update."""

        model = CourseTypeF.create()
        new_model_data = {
            'name': 'new Course Type name',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)
            self.assertTrue(model.name == 'new Course Type name')

    def test_create_CourseType_non_unique_slug(self):
        """Test create CourseType instances with the same name.

        The duplicate slug must be allowed.
        """
        long_name = 'Very long long course type name, more than 50 characters'
        course_type_1 = CourseTypeF.create(name=long_name)
        self.assertEqual(len(course_type_1.slug), 50)
        course_type_2 = CourseTypeF.create(name=long_name)
        self.assertEqual(course_type_1.slug, course_type_2.slug)
        self.assertNotEqual(course_type_1.pk, course_type_2.pk)


class TestCourseConvener(TestCase):
    """Test course convener model."""

    def setUp(self):
        """Set up before test."""

        pass

    def test_Course_Convener_create(self):
        """Test course convener model creation."""

        model = CourseConvenerF.create()
        new_model_data = {
            'title': 'new Course Convener Title',
            'degree': 'new Course Convener Degree',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)
            self.assertTrue(model.title == 'new Course Convener Title')
            self.assertTrue(model.degree == 'new Course Convener Degree')
            self.assertTrue(model.is_active)

        # check if PK exists.
        self.assertTrue(model.pk is not None)

    def test_Course_Convener_delete(self):
        """Test course convener model delete."""

        model = CourseConvenerF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)


class TestCourseAttendee(TestCase):
    """Test course convener model."""

    def setUp(self):
        """Set up before test."""

        pass

    def test_Course_Attendee_create(self):
        """Test course convener model creation."""

        model = CourseAttendeeF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

    def test_Course_Attendee_delete(self):
        """Test course convener model delete."""

        model = CourseAttendeeF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)


class TestStatus(TestCase):
    """Test status model."""

    def setUp(self):
        """Set up before test."""

        pass

    def test_Status_create(self):
        """Test status model creation."""

        model = StatusF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

    def test_Status_delete(self):
        """Test status model deletion."""

        model = StatusF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)

    def test_Status_update(self):
        """Test status model update."""

        model = StatusF.create()
        new_model_data = {
            'name': 'new Status name',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated.
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)
            self.assertTrue(model.name == 'new Status name')


class TestValidateEmailAddress(TestCase):
    """Test validate_email_address function."""

    def test_validation_failed_must_raise_ValidationError(self):
        from certification.models import validate_email_address
        email = 'email@wrongdomain'
        msg = f'{email} is not a valid email address'
        with self.assertRaisesMessage(ValidationError, msg):
            validate_email_address(email)


class TestExternalReviewer(TestCase):

    def test_External_Reviewer_create(self):
        """Test external reviewer model creation."""

        model = ExternalReviewerF.create()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

    def test_External_Reviewer_expire(self):
        from django.contrib.sessions.backends.db import SessionStore

        s = SessionStore()
        s.create()
        model = ExternalReviewerF.create(
            session_key=s.session_key
        )

        self.assertFalse(model.session_expired)

        model_with_no_session = ExternalReviewerF.create()
        self.assertTrue(model_with_no_session.session_expired)
        self.assertTrue(
            str(model),
            model.email
        )


class TestChecklist(TestCase):
    """Test checklist model."""

    def setUp(self):
        """Set up before test."""

        pass

    def test_Checklist_create(self):
        """Test checklist model creation."""

        model = ChecklistF.create()

        history = model.history.earliest()
        user = UserF.create()
        history.history_user = user
        history.save()

        # check if PK exists.
        self.assertTrue(model.pk is not None)

        # check if model attributes exists.
        self.assertEqual(model.creator, user)

        self.assertEqual(
            str(model),
            model.question
        )

        self.assertEqual(
            model.target,
            ''
        )

        history.delete()

        self.assertIsNone(model.creator)

    def test_Checklist_delete(self):
        """Test checklist model deletion."""

        model = ChecklistF.create()
        model.delete()

        # check if deleted.
        self.assertTrue(model.pk is None)
