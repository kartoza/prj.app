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


class CertifyingOrganisationF(factory.django.DjangoModelFactory):
    """
    Certifying organisation model factory.
    """
    class Meta:
        model = CertifyingOrganisation

    name = factory.sequence(lambda n: u'Test certifying '
                                      u'organisation name %s' % n)
    organisation_email = factory.sequence(lambda n: u'Test address %s' % n)
    organisation_phone = factory.sequence(lambda n: u'Test phone %s' % n)
    approved = True
    project = factory.SubFactory('base.tests.model_factories.ProjectF')


class CourseTypeF(factory.django.DjangoModelFactory):
    """
    Course type model factory.
    """
    class Meta:
        model = CourseType

    name = factory.sequence(lambda n: u'Test course type name %s' % n)

    @factory.post_generation
    # simple many to many relationship
    def course(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them.
            for courses in extracted:
                self.course.add(courses)


class CertificateF(factory.django.DjangoModelFactory):
    """
    Certificate model factory.
    """
    class Meta:
        model = Certificate

    id_id = u'123AAA'


class AttendeeF(factory.django.DjangoModelFactory):
    """
    Certificate model factory.
    """
    class Meta:
        model = Attendee

    firstname = factory.sequence(lambda n: u'Test attendee firstname %s' % n)
    surname = factory.sequence(lambda n: u'Test surname %s' % n)
    email = factory.sequence(lambda n: u'Test email %s' % n)
    # one to one relationship
    certificate = factory.SubFactory(CertificateF)

    # @factory.post_generation
    # # simple many to many relationship
    # def certificate(self, create, extracted, **kwargs):
    #     if not create:
    #         # Simple build, do nothing.
    #         return
    #
    #     if extracted:
    #         # A list of groups were passed in, use them
    #         for certificate in extracted:
    #             self.certificate.add(certificate)


class CourseF(factory.django.DjangoModelFactory):
    """
    Course model factory.
    """
    class Meta:
        model = Course

    name = factory.sequence(lambda n: u'Test course name %s' % n)

    @factory.post_generation
    # simple many to many relationship
    def course_attendee(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them.
            for attendees in extracted:
                self.course_attendee.add(attendees)

    @factory.post_generation
    # simple many to many relationship
    def certificate(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them.
            for _certificate in extracted:
                self.certificate.add(_certificate)


class TrainingCenterF(factory.django.DjangoModelFactory):
    """
    Training center model factory.
    """
    class Meta:
        model = TrainingCenter

    name = factory.sequence(lambda n: u'Test training center name %s' % n)
    email = factory.sequence(lambda n: u'Test email %s' % n)
    Address = u'Test address'
    phone = factory.sequence(lambda n: u'Test phone %s' % n)

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


class CourseConvenerF(factory.django.DjangoModelFactory):
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
