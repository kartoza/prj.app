# coding=utf-8
from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView)
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
        kwargs.update({
            'user': self.request.user,
            'course': self.course,
        })
        return kwargs
