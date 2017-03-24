# coding=UTF-8
"""Model admin class definitions."""

# import reversion
from django.contrib import admin
from certification.models.certificate import Certificate
from certification.models.course import Course
from certification.models.certifying_organisation import CertifyingOrganisation
from certification.models.training_center import TrainingCenter
from certification.models.course_convener import CourseConvener
from certification.models.course_type import CourseType
from certification.models.attendee import Attendee


class CertificateAdmin(admin.ModelAdmin):
    """Certificate admin model."""
    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class AttendeeAdmin(admin.ModelAdmin):
    """Attendee admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class CourseAdmin(admin.ModelAdmin):
    """Course admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class CourseTypeAdmin(admin.ModelAdmin):
    """Course type admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class TrainingCenterAdmin(admin.ModelAdmin):
    """Training center admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class CourseConvenerAdmin(admin.ModelAdmin):
    """Course convener admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class CertifyingOrganisationAdmin(admin.ModelAdmin):
    """Certifying organisation admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        qs = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(TrainingCenter, TrainingCenterAdmin)
admin.site.register(CourseConvener, CourseConvenerAdmin)
admin.site.register(CertifyingOrganisation, CertifyingOrganisationAdmin)
