# coding=utf-8
from datetime import timedelta, datetime

from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView)
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin
from base.models import Project
from ..models import (
    CertifyingOrganisation,
    Course,
    CourseAttendee,
    Certificate)
from ..forms import CourseForm
from certification.utilities import check_slug


class CourseMixin(object):
    """Mixin class to provide standard settings for Course."""

    model = Course
    form_class = CourseForm


class CourseCreateView(LoginRequiredMixin, CourseMixin, CreateView):
    """Create view for Course."""

    context_object_name = 'course'
    template_name = 'course/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Certifying Organisation detail page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.certifying_organisation.project.slug,
            'slug': self.object.certifying_organisation.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CourseCreateView, self).get_context_data(**kwargs)
        context['courses'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        context['organisation_slug'] = self.kwargs.pop('organisation_slug')
        context['organisation'] = (
            CertifyingOrganisation.objects.get(
                slug=context['organisation_slug'])
        )
        context['project_slug'] = self.kwargs.pop('project_slug')
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseCreateView, self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation,
        })
        return kwargs


class CourseUpdateView(LoginRequiredMixin, CourseMixin, UpdateView):
    """Update view for Course."""

    context_object_name = 'course'
    template_name = 'course/update.html'

    def get(self, request, *args, **kwargs):
        """Get the organisation_slug from the URL
        and define the Organisation.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        try:
            self.certifying_organisation = \
                CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        except CertifyingOrganisation.DoesNotExist:
            raise Http404(
                'Sorry! We could not find your certifying organisation!')

        try:
            self.object = self.get_object()
        except PermissionDenied:
            # Return to organisation details page when permission to edit
            # is denied.
            return HttpResponseRedirect(
                reverse('certifyingorganisation-detail', kwargs={
                    'project_slug': self.certifying_organisation.project.slug,
                    'slug': self.certifying_organisation.slug
                }))

        return super(CourseUpdateView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseUpdateView, self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(CourseUpdateView, self).get_context_data(**kwargs)
        context['courses'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        context['organisation_slug'] = self.kwargs.pop('organisation_slug')
        context['organisation'] = (
            CertifyingOrganisation.objects.get(
                slug=context['organisation_slug'])
        )
        context['project_slug'] = self.kwargs.pop('project_slug')
        return context

    def get_queryset(self):
        """Get the queryset for this view.
            In front end, only staff, organisation owners and course convener
            can see the edit button.

        :returns: All Course objects
        :rtype: QuerySet
        """

        qs = Course.objects.all()
        return qs

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the Certifying Organisation detail page.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.certifying_organisation.project.slug,
            'slug': self.object.certifying_organisation.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""

        try:
            return super(CourseUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Course Convener is already exists!')

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a course
            within the organisation.
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            organisation_slug = self.kwargs.get('organisation_slug', None)
            if slug and organisation_slug:
                try:
                    certifying_organisation = \
                        CertifyingOrganisation.objects.get(
                            slug=organisation_slug)
                except CertifyingOrganisation.DoesNotExist:
                    raise Http404(
                        'Sorry! We could not find your '
                        'certifying organisation!')
                try:
                    obj = queryset.get(
                        certifying_organisation=certifying_organisation,
                        slug=slug)
                    return obj
                except Course.DoesNotExist:
                    raise Http404('Sorry! We could not find your course!')
                except Course.MultipleObjectsReturned:
                    # Update the slug for the latest object when multiple
                    # objects with the same slug are found and raise
                    # Permission Denied
                    new_slug = check_slug(queryset, slug)
                    objects = queryset.filter(
                        certifying_organisation=certifying_organisation,
                        slug=slug)
                    latest_obj = len(objects) - 1
                    objects[latest_obj].slug = new_slug
                    objects[latest_obj].save()
                    raise PermissionDenied
            else:
                raise Http404('Sorry! We could not find your course!')


class CourseDeleteView(LoginRequiredMixin, CourseMixin, DeleteView):
    """Delete view for Course."""

    context_object_name = 'course'
    template_name = 'course/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the organisation_slug from the URL
        and define the Organisation.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        try:
            self.certifying_organisation = \
                CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        except CertifyingOrganisation.DoesNotExist:
            raise Http404(
                'Sorry! We could not find your certifying organisation!')

        try:
            self.object = self.get_object()
        except PermissionDenied:
            # Return to organisation details page when permission to delete
            # is denied.
            return HttpResponseRedirect(
                reverse('certifyingorganisation-detail', kwargs={
                    'project_slug': self.certifying_organisation.project.slug,
                    'slug': self.certifying_organisation.slug
                }))

        return super(CourseDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the organisation_slug from the URL.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        return super(CourseDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation detail page.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.certifying_organisation.project.slug,
            'slug': self.object.certifying_organisation.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Course queryset filtered by Organisation
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated:
            raise Http404
        qs = Course.objects.filter(
            certifying_organisation=self.certifying_organisation)
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a course
            within the organisation.
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            organisation_slug = self.kwargs.get('organisation_slug', None)
            if slug and organisation_slug:
                try:
                    certifying_organisation = \
                        CertifyingOrganisation.objects.get(
                            slug=organisation_slug)
                except CertifyingOrganisation.DoesNotExist:
                    raise Http404(
                        'Sorry! We could not find your '
                        'certifying organisation!')
                try:
                    obj = queryset.get(
                        certifying_organisation=certifying_organisation,
                        slug=slug)
                    return obj
                except Course.DoesNotExist:
                    raise Http404('Sorry! We could not find your course!')
                except Course.MultipleObjectsReturned:
                    # Update the slug for the latest object when multiple
                    # objects with the same slug are found and raise
                    # Permission Denied
                    new_slug = check_slug(queryset, slug)
                    objects = queryset.filter(
                        certifying_organisation=certifying_organisation,
                        slug=slug)
                    latest_obj = len(objects) - 1
                    objects[latest_obj].slug = new_slug
                    objects[latest_obj].save()
                    raise PermissionDenied
            else:
                raise Http404('Sorry! We could not find your course!')


class CourseDetailView(CourseMixin, DetailView):
    """Detail view for Course."""

    context_object_name = 'course'
    template_name = 'course/detail.html'

    def get(self, request, *args, **kwargs):
        """Get the organisation_slug from the URL
        and define the Organisation.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        try:
            self.certifying_organisation = \
                CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        except CertifyingOrganisation.DoesNotExist:
            raise Http404(
                'Sorry! We could not find your certifying organisation!')

        try:
            self.object = self.get_object()
        except PermissionDenied:
            # Return to organisation details page when permission to view
            # is denied.
            return HttpResponseRedirect(
                reverse('certifyingorganisation-detail', kwargs={
                    'project_slug': self.certifying_organisation.project.slug,
                    'slug': self.certifying_organisation.slug
                }))

        return super(CourseDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.slug = self.kwargs.get('slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        self.course = Course.objects.get(slug=self.slug)
        context = super(
            CourseDetailView, self).get_context_data(**kwargs)

        attendees = (
            CourseAttendee.objects.filter(course=self.course)
        )
        for course_attendee in attendees:
            course_attendee.editable = False
            certificate = Certificate.objects.filter(
                course=self.course,
                attendee=course_attendee.attendee
            ).first()
            if certificate:
                course_attendee.editable = (
                    certificate.issue_date and
                    certificate.issue_date +
                    timedelta(days=7) > datetime.today().date()
                )
            else:
                course_attendee.editable = True
        context['attendees'] = attendees

        context['certificates'] = dict(
            Certificate.objects.filter(
                course=self.course
            ).values_list('attendee', 'certificateID')
        )
        context['paid_certificates'] = \
            Certificate.objects.filter(
                course=self.course, is_paid=True).values_list(
                'attendee', flat=True)
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
            context['project'] = context['the_project']
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all course in the
            corresponding organisation.
        :rtype: QuerySet
        """

        qs = Course.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a course
            within the organisation.
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            organisation_slug = self.kwargs.get('organisation_slug', None)
            if slug and organisation_slug:
                try:
                    certifying_organisation = \
                        CertifyingOrganisation.objects.get(
                            slug=organisation_slug)
                except CertifyingOrganisation.DoesNotExist:
                    raise Http404(
                        'Sorry! We could not find your '
                        'certifying organisation!')
                try:
                    obj = queryset.get(
                        certifying_organisation=certifying_organisation,
                        slug=slug)
                    return obj
                except Course.DoesNotExist:
                    raise Http404('Sorry! We could not find your course!')
                except Course.MultipleObjectsReturned:
                    # Update the slug for the latest object when multiple
                    # objects with the same slug are found and raise
                    # Permission Denied
                    new_slug = check_slug(queryset, slug)
                    objects = queryset.filter(
                        certifying_organisation=certifying_organisation,
                        slug=slug)
                    latest_obj = len(objects) - 1
                    objects[latest_obj].slug = new_slug
                    objects[latest_obj].save()
                    raise PermissionDenied
            else:
                raise Http404('Sorry! We could not find your course!')
