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


class CertifyingOrganisationF(factory.django.DjangoModelFactory):
    """
    Certifying organisation model factory.
    """
    class Meta:
        model = CertifyingOrganisation

    name = factory.sequence(lambda n: u'Test certifying '
                                      u'organisation name %s' % n)
    organisation_email = factory.sequence(lambda n: u'Test email %s' % n)
    organisation_phone = factory.sequence(lambda n: u'Test phone %s' % n)
    address = factory.sequence(lambda n: u'Test address %s' % n)
    #project = factory.SubFactory('base.tests.model_factories.ProjectF')
    author = factory.SubFactory(UserF)
    approved = True


class CourseConvenerF(factory.django.DjangoModelFactory):
    """
    Course convener model factory.
    """

    class Meta:
        model = CourseConvener

    #project = factory.SubFactory('base.tests.model_factories.ProjectF')
    author = factory.SubFactory(UserF)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)


class TrainingCenterF(factory.django.DjangoModelFactory):
    """
    Training center model factory.
    """
    class Meta:
        model = TrainingCenter

    name = factory.sequence(lambda n: u'Test training center name %s' % n)
    email = factory.sequence(lambda n: u'Test email %s' % n)
    address = u'Test address'
    phone = factory.sequence(lambda n: u'Test phone %s' % n)

    #project = factory.SubFactory('base.tests.model_factories.ProjectF')
    author = factory.SubFactory(UserF)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)


class CourseTypeF(factory.django.DjangoModelFactory):
    """
    Course type model factory.
    """
    class Meta:
        model = CourseType

    name = factory.sequence(lambda n: u'Test course type name %s' % n)

    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)
    #project = factory.SubFactory('base.tests.model_factories.ProjectF')
    author = factory.SubFactory(UserF)


class CourseF(factory.django.DjangoModelFactory):
    """
    Course model factory.
    """
    class Meta:
        model = Course

    name = factory.sequence(lambda n: u'Test course name %s' % n)

    #project = factory.SubFactory('base.tests.model_factories.ProjectF')
    author = factory.SubFactory(UserF)
    course_convener = factory.SubFactory(CourseConvenerF)
    certifying_organisation = factory.SubFactory(CertifyingOrganisationF)
    course_type = factory.SubFactory(CourseTypeF)
    training_center = factory.SubFactory(TrainingCenterF)


class CourseAttendeeF(factory.django.DjangoModelFactory):
    """
    Course attendee model factory.
    """

    class Meta:
        model = CourseAttendee

    training_center = factory.SubFactory(TrainingCenterF)
    course = factory.SubFactory(CourseF)
    #project = factory.SubFactory('base.tests.model_factories.ProjectF')
    author = factory.SubFactory(UserF)

    @factory.post_generation
    # simple many to many relationship
    def attendee(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for _attendee in extracted:
                self.attendee.add(_attendee)


class CertificateF(factory.django.DjangoModelFactory):
    """
    Certificate model factory.
    """
    class Meta:
        model = Certificate

    certificateID = u'123AAA'
    #project = factory.SubFactory('base.tests.model_factories.ProjectF')
    author = factory.SubFactory(UserF)
    course_attendee = factory.SubFactory(CourseAttendeeF)
    course = factory.SubFactory(CourseF)


class AttendeeF(factory.django.DjangoModelFactory):
    """
    Certificate model factory.
    """
    class Meta:
        model = Attendee

    firstname = factory.sequence(lambda n: u'Test attendee firstname %s' % n)
    surname = factory.sequence(lambda n: u'Test surname %s' % n)
    email = factory.sequence(lambda n: u'Test email %s' % n)
    #project = factory.SubFactory('base.tests.model_factories.ProjectF')
    author = factory.SubFactory(UserF)
