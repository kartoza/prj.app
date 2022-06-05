# coding=UTF-8
"""Model admin class definitions."""

from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from certification.models.certificate import Certificate
from certification.models.certificate_type import CertificateType
from certification.models.course import Course
from certification.models.training_center import TrainingCenter
from certification.models.course_convener import CourseConvener
from certification.models.course_type import CourseType
from certification.models.attendee import Attendee
from certification.models.course_attendee import CourseAttendee
from certification.models.certifying_organisation import CertifyingOrganisation
from certification.models.organisation_certificate import \
    CertifyingOrganisationCertificate
from certification.models.status import Status
from certification.models.checklist import Checklist
from certification.models.organisation_checklist import OrganisationChecklist
from certification.models.external_reviewer import ExternalReviewer


class CertificateAdmin(admin.ModelAdmin):
    """Certificate admin model."""

    list_display = ('certificateID', 'course')
    search_fields = ('certificateID', 'course__name',)
    readonly_fields = ('issue_date',)

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class CertificateTypeAdmin(admin.ModelAdmin):
    """CertificateType admin model."""

    list_display = ('name', 'wording', 'order')
    list_editable = ('order', )
    search_fields = ('name', 'wording')
    ordering = ('order', )


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


class CertifyingOrganisationCertificateAdminInline(admin.TabularInline):
    model = CertifyingOrganisationCertificate
    extra = 0


class CertifyingOrganisationCertificateAdmin(SimpleHistoryAdmin):
    history_list_display = ['issued', 'valid']


class CertifyingOrganisationAdmin(SimpleHistoryAdmin):
    """Certifying organisation admin model."""

    filter_horizontal = ('organisation_owners',)
    search_fields = ['name']
    list_display = ('name', 'project', 'country', 'approved', 'rejected')
    list_filter = ('country', 'approved', 'rejected', 'status')
    inlines = (CertifyingOrganisationCertificateAdminInline, )
    history_list_display = ['status', 'remarks']

    def queryset(self, request):
        """Ensure we use the correct manager.

        :param request: HttpRequest object
        """
        query_set = self.model.objects
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'order')


class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('project', 'question', 'target', 'active')


class OrganisationChecklistAdmin(admin.ModelAdmin):
    list_display = ('organisation', 'checklist_question',
                    'checked', 'checklist_target')
    raw_id_fields = ('organisation', 'submitter', )
    list_filter = ('checklist_target', )


class ExternalReviewerAdmin(admin.ModelAdmin):
    list_display = (
        'certifying_organisation',
        'email',
        'session_expired'
    )


admin.site.register(Certificate, CertificateAdmin)
admin.site.register(CertificateType, CertificateTypeAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(TrainingCenter, TrainingCenterAdmin)
admin.site.register(CourseConvener, CourseConvenerAdmin)
admin.site.register(CertifyingOrganisation, CertifyingOrganisationAdmin)
admin.site.register(CourseAttendee, CourseAttendeeAdmin)
admin.site.register(
    CertifyingOrganisationCertificate, CertifyingOrganisationCertificateAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(OrganisationChecklist, OrganisationChecklistAdmin)
admin.site.register(ExternalReviewer, ExternalReviewerAdmin)
