# coding=utf-8
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView)
from django.http import Http404
from braces.views import LoginRequiredMixin
from ..models import (
    CourseAttendee,
    CertifyingOrganisation,
    Course)
from ..forms import CourseAttendeeForm


class CourseAttendeeMixin(object):
    """Mixin class to provide standard settings for Attendee."""

    model = CourseAttendee
    form_class = CourseAttendeeForm


class CourseAttendeeCreateView(
        LoginRequiredMixin,
        CourseAttendeeMixin, CreateView):
    """Create view for Course Attendee."""

    context_object_name = 'courseattendee'
    template_name = 'course_attendee/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Course detail page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('course-detail', kwargs={
            'project_slug': self.project_slug,
            'organisation_slug': self.organisation_slug,
            'slug': self.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CourseAttendeeCreateView, self).get_context_data(**kwargs)
        context['certifyingorganisation'] = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        context['course'] = Course.objects.get(slug=self.slug)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseAttendeeCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.slug = self.kwargs.get('slug', None)
        self.course = Course.objects.get(slug=self.slug)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'course': self.course,
            'certifying_organisation': self.certifying_organisation,
        })
        return kwargs


class CourseAttendeeDeleteView(
        LoginRequiredMixin,
        CourseAttendeeMixin,
        DeleteView):
    """Delete view for Course Attendee."""

    context_object_name = 'courseattendee'
    template_name = 'course_attendee/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the course_slug and course attendee pk from the URL
        and define the course.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.course_slug = self.kwargs.get('course_slug', None)
        self.pk = self.kwargs.get('pk', None)
        self.course = Course.objects.get(slug=self.course_slug)
        return super(
            CourseAttendeeDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the project_slug, organisation_slug, course_slug from the URL.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.course_slug = self.kwargs.get('course_slug', None)
        self.course = Course.objects.get(slug=self.course_slug)
        return super(
            CourseAttendeeDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Course detail page.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('course-detail', kwargs={
            'project_slug': self.project_slug,
            'organisation_slug': self.organisation_slug,
            'slug': self.course_slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Course Attendee queryset filtered by Course
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated:
            raise Http404
        qs = CourseAttendee.objects.filter(course=self.course)
        return qs
