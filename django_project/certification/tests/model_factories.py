# coding=utf-8
"""Factories for building model instances for testing."""

import factory

from certification.models import (
    Certificate,
    CertificateType,
    ProjectCertificateType,
    Attendee,
    Course,
    CourseType,
    CourseConvener,
    CertifyingOrganisation,
    TrainingCenter,
    CourseAttendee,
    Status,
    CertifyingOrganisationCertificate,
    Checklist, OrganisationChecklist, ExternalReviewer,
)
from core.model_factories import UserF
from base.tests.model_factories import ProjectF


class CertifyingOrganisationF(factory.django.DjangoModelFactory):
    """Certifying organisation model factory."""

    class Meta:
        model = CertifyingOrganisation

    name = factory.sequence(
        lambda n: u'Test certifying organisation name %s' % n)
    organisation_email = factory.sequence(lambda n: u'Test email %s' % n)
    organisation_phone = factory.sequence(lambda n: u'Test phone %s' % n)
    address = factory.sequence(lambda n: u'Test address %s' % n)
    project = factory.SubFactory(ProjectF)
    approved = True


class CertifyingOrganisationCertificateF(factory.django.DjangoModelFactory):
    class Meta:
        model = CertifyingOrganisationCertificate

    certificateID = factory.sequence(lambda n: u'cert-%s' % n)
    author = factory.SubFactory(UserF)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)


class CourseConvenerF(factory.django.DjangoModelFactory):
    """Course convener model factory."""

    class Meta:
        model = CourseConvener

    user = factory.SubFactory(UserF)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)


class TrainingCenterF(factory.django.DjangoModelFactory):
    """Training center model factory."""

    class Meta:
        model = TrainingCenter

    name = factory.sequence(lambda n: u'Test training center name %s' % n)
    email = factory.sequence(lambda n: u'Test email %s' % n)
    address = u'Test address'
    phone = factory.sequence(lambda n: u'Test phone %s' % n)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)
    author = factory.SubFactory(UserF)


class CourseTypeF(factory.django.DjangoModelFactory):
    """Course type model factory."""

    class Meta:
        model = CourseType

    name = factory.sequence(lambda n: u'Test course type name %s' % n)
    description = factory.sequence(lambda n: u'Course type description %s' % n)
    instruction_hours = factory.sequence(lambda n: u'Instruction hours %s' % n)
    coursetype_link = factory.sequence(lambda n: u'Course type link %s' % n)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)
    author = factory.SubFactory(UserF)


class CertificateTypeF(factory.django.DjangoModelFactory):
    """CertificateType model factory."""

    class Meta:
        model = CertificateType

    name = factory.sequence(lambda n: 'Test certificate type name %s' % n)
    description = factory.sequence(
        lambda n: 'Description certificate type %s' % n)
    wording = factory.sequence(
        lambda n: 'Wording certificate type %s' % n)


class CourseF(factory.django.DjangoModelFactory):
    """Course model factory."""

    class Meta:
        model = Course

    name = factory.sequence(lambda n: u'Test course name %s' % n)
    language = factory.sequence(
        lambda n: u'Test course language %s' % n)
    trained_competence = factory.sequence(
        lambda n: u'Test trained competence %s' % n)
    course_convener = factory.SubFactory(CourseConvenerF)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)
    course_type = factory.SubFactory(CourseTypeF)
    training_center = factory.SubFactory(TrainingCenterF)
    author = factory.SubFactory(UserF)
    certificate_type = factory.SubFactory(CertificateTypeF)


class AttendeeF(factory.django.DjangoModelFactory):
    """Attendee model factory."""

    class Meta:
        model = Attendee

    firstname = factory.sequence(lambda n: u'Test attendee firstname %s' % n)
    surname = factory.sequence(lambda n: u'Test surname %s' % n)
    email = factory.sequence(lambda n: u'Test email %s' % n)
    slug = factory.sequence(lambda n: u'test attendee slug %s' % n)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)
    author = factory.SubFactory(UserF)


class CourseAttendeeF(factory.django.DjangoModelFactory):
    """Course attendee model factory."""

    class Meta:
        model = CourseAttendee

    course = factory.SubFactory(CourseF)
    author = factory.SubFactory(UserF)
    attendee = factory.SubFactory(AttendeeF)


class ProjectCertificateTypeF(factory.django.DjangoModelFactory):
    """ProjectCertificateType model factory."""

    class Meta:
        model = ProjectCertificateType

    project = factory.SubFactory(ProjectF)
    certificate_type = factory.SubFactory(CertificateTypeF)


class CertificateF(factory.django.DjangoModelFactory):
    """Certificate model factory."""

    class Meta:
        model = Certificate

    certificateID = u'ProjectTest-1'
    course = factory.SubFactory(CourseF)
    attendee = factory.SubFactory(AttendeeF)
    author = factory.SubFactory(UserF)


class StatusF(factory.django.DjangoModelFactory):
    """Certificate model factory."""

    class Meta:
        model = Status

    name = factory.sequence(lambda n: u'Test status %s' % n)
    project = factory.SubFactory(ProjectF)


class ChecklistF(factory.django.DjangoModelFactory):
    class Meta:
        model = Checklist

    question = factory.sequence(lambda n: u'Test question %s' % n)
    project = factory.SubFactory(ProjectF)


class OrganisationChecklistF(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganisationChecklist

    checklist = factory.SubFactory(ChecklistF)
    organisation = factory.SubFactory(CertifyingOrganisationF)
    checklist_question = factory.sequence(
        lambda n: 'Question %s' % n)


class ExternalReviewerF(factory.django.DjangoModelFactory):
    class Meta:
        model = ExternalReviewer

    certifying_organisation = factory.SubFactory(
        CertifyingOrganisationF
    )
    session_key = factory.Sequence(
        lambda n: 'session %s' % n
    )
    email = factory.Sequence(
        lambda n: 'email%s@email.com' % n
    )
