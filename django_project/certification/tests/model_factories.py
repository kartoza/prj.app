# coding=utf-8
"""Factories for building model instances for testing."""

import factory

from certification.models import (
    Certificate,
    Attendee,
    Course,
    CourseType,
    CourseConvener,
    CertifyingOrganisation,
    TrainingCenter,
    CourseAttendee)
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


class CourseF(factory.django.DjangoModelFactory):
    """Course model factory."""

    class Meta:
        model = Course

    name = factory.sequence(lambda n: u'Test course name %s' % n)
    course_language = factory.sequence(
        lambda n: u'Test course language %s' % n)
    course_convener = factory.SubFactory(CourseConvenerF)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)
    course_type = factory.SubFactory(CourseTypeF)
    training_center = factory.SubFactory(TrainingCenterF)
    author = factory.SubFactory(UserF)


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


class CertificateF(factory.django.DjangoModelFactory):
    """Certificate model factory."""

    class Meta:
        model = Certificate

    certificateID = u'ProjectTest-1'
    course = factory.SubFactory(CourseF)
    attendee = factory.SubFactory(AttendeeF)
    author = factory.SubFactory(UserF)
