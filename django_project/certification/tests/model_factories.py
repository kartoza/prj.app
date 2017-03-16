# coding=utf-8
"""Factories for building model instances for testing"""

import factory
from certification.models import (
    Certificate,
    Attendee,
    Course,
    CourseType,
    CourseConvener,
    CertifyingOrganisation,
    TrainingCenter)


class CertifyingOrganisationF(factory.Factory):
    """
    Certifying organisation model factory.
    """
    class Meta:
        model = CertifyingOrganisation

    name = factory.sequence(lambda n: u'Test certifying organisation name %s' % n)
    organisation_email = factory.sequence(lambda n: u'Test address %s' % n)
    organisation_phone = factory.sequence(lambda n: u'Test phone %s' % n)
    approved = True
    project = factory.SubFactory('base.tests.model_factories.ProjectF')


class CourseTypeF(factory.Factory):
    """
    Course type model factory.
    """
    class Meta:
        model = CourseType

    name = factory.sequence(lambda n: u'Test course type name %s' % n)
    # course = factory.SubFactory(CourseF)

    @factory.post_generation
    # simple many to many relationship
    def course(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for courses in extracted:
                self.course.add(courses)


class CertificateF(factory.Factory):
    """
    Certificate model factory.
    """
    class Meta:
        model = Certificate

    id = factory.sequence(lambda n: u'Test ID %s' % n)


class AttendeeF(factory.Factory):
    """
    Certificate model factory.
    """
    class Meta:
        model = Attendee

    firstname = factory.sequence(lambda n: u'Test attendee firstname %s' % n)
    surname = factory.sequence(lambda n: u'Test surname %s' % n)
    email = factory.sequence(lambda n: u'Test email %s' % n)
    # certificate = factory.SubFactory(CertificateF)

    @factory.post_generation
    # simple many to many relationship
    def certificate(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for _certificate in extracted:
                self.certificate.add(_certificate)


class CourseF(factory.Factory):
    """
    Course model factory.
    """
    class Meta:
        model = Course

    name = factory.sequence(lambda n: u'Test course name %s' % n)
    # course_attendee = factory.SubFactory(AttendeeF)
    # certificate = factory.SubFactory(CertificateF)

    @factory.post_generation
    # simple many to many relationship
    def course_attendee(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for attendees in extracted:
                self.course_attendee.add(attendees)

    @factory.post_generation
    # simple many to many relationship
    def certificate(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for _certificate in extracted:
                self.certificate.add(_certificate)


class TrainingCenterF(factory.Factory):
    """
    Training center model factory.
    """
    class Meta:
        model = TrainingCenter

    name = factory.sequence(lambda n: u'Test training center name %s' % n)
    email = factory.sequence(lambda n: u'Test email %s' % n)
    address = factory.sequence(lambda n: u'Test address %s' % n)
    phone = factory.sequence(lambda n: u'Test phone %s' % n)
    # course = factory.SubFactory(CourseF)

    @factory.post_generation
    # simple many to many relationship
    def course(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for _course in extracted:
                self.course.add(_course)


class CourseConvenerF(factory.Factory):
    """
    Course convener model factory.
    """
    class Meta:
        model = CourseConvener

    # course = factory.SubFactory(CourseF)

    @factory.post_generation
    # simple many to many relationship
    def course(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for _course in extracted:
                self.course.add(_course)