# coding=UTF-8
"""Model admin class definitions."""

from django.contrib import admin
from models import (
    Certificate, Course, CertifyingOrganisation,
    TrainingCenter, CourseConvener, CourseType,
    Attendee)
import reversion


class CertificateAdmin(reversion.VersionAdmin):
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


class AttendeeAdmin(reversion.VersionAdmin):
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


class CourseAdmin(reversion.VersionAdmin):
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


class CourseTypeAdmin(reversion.VersionAdmin):
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


class TrainingCenterAdmin(reversion.VersionAdmin):
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


class CourseConvenerAdmin(reversion.VersionAdmin):
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


class CertifyingOrganisationAdmin(reversion.VersionAdmin):
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