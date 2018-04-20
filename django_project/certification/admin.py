# coding=UTF-8
"""Model admin class definitions."""

from django.contrib.gis import admin
from certification.models.certificate import Certificate
from certification.models.course import Course
from certification.models.training_center import TrainingCenter
from certification.models.course_convener import CourseConvener
from certification.models.course_type import CourseType
from certification.models.attendee import Attendee
from certification.models.course_attendee import CourseAttendee
from certification.models.certifying_organisation import CertifyingOrganisation


class CertificateAdmin(admin.ModelAdmin):
    """Certificate admin model."""

    list_display = ('__unicode__', 'course')
    search_fields = ('certificateID', 'course__name',)

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class AttendeeAdmin(admin.ModelAdmin):
    """Attendee admin model."""
    list_display = ('firstname', 'surname', 'email', 'certifying_organisation')
    search_fields = ['firstname', 'surname']

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class CourseAttendeeAdmin(admin.ModelAdmin):
    """Certificate admin model."""
    list_display = ('course', 'attendee', 'author')

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class CourseAdmin(admin.ModelAdmin):
    """Course admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class CourseTypeAdmin(admin.ModelAdmin):
    """Course type admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class TrainingCenterAdmin(admin.GeoModelAdmin):
    """Training center admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class CourseConvenerAdmin(admin.ModelAdmin):
    """Course convener admin model."""

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class CertifyingOrganisationAdmin(admin.ModelAdmin):
    """Certifying organisation admin model."""

    filter_horizontal = ('organisation_owners',)
    search_fields = ['name']

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(TrainingCenter, TrainingCenterAdmin)
admin.site.register(CourseConvener, CourseConvenerAdmin)
admin.site.register(CertifyingOrganisation, CertifyingOrganisationAdmin)
admin.site.register(CourseAttendee, CourseAttendeeAdmin)
