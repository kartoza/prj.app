# coding=utf-8
import csv
from django.db import transaction
from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView, FormView)
from braces.views import LoginRequiredMixin, FormMessagesMixin
from ..models import Attendee, CertifyingOrganisation, CourseAttendee
from ..forms import AttendeeForm
from ..forms import CsvAttendeeForm
from ..models.course_attendee import Course


class AttendeeMixin(object):
    """Mixin class to provide standard settings for Attendee."""

    model = Attendee
    form_class = AttendeeForm


class AttendeeCreateView(
        LoginRequiredMixin,
        AttendeeMixin, CreateView):
    """Create view for Attendee."""

    context_object_name = 'attendee'
    template_name = 'attendee/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the create course attendee page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('courseattendee-create', kwargs={
            'project_slug': self.project_slug,
            'organisation_slug': self.organisation_slug,
            'slug': self.course_slug,
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            AttendeeCreateView, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(AttendeeCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.course_slug = self.kwargs.get('slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation
        })
        return kwargs


class CsvUploadView(FormMessagesMixin, LoginRequiredMixin,
                    FormView):
    """
    Allow upload of attendees through CSV file.
    """

    context_object_name = 'csvupload'
    form_class = CsvAttendeeForm
    template_name = 'attendee/upload_attendee_csv.html'

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
            'slug': self.slug,
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CsvUploadView, self).get_context_data(**kwargs)
        context['certifyingorganisation'] = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        context['course'] = Course.objects.get(slug=self.slug)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CsvUploadView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.slug = self.kwargs.get('slug', None)
        self.course = Course.objects.get(slug=self.slug)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            # 'user': self.request.user,
            # 'course': self.course,
            # 'certifying_organisation': self.certifying_organisation,
        })
        return kwargs

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """Get form instance from upload.

           After successful creation of the object,
           the User will be redirected to the create
           course attendee page.

          :returns: URL
          :rtype: HttpResponse
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        attendees_file = request.FILES.get('file')
        course = Course.objects.get(slug=self.slug)
        if form.is_valid():
            if attendees_file:
                reader = csv.reader(attendees_file, delimiter=',')
                next(reader)
                attendee_count = 0
                course_attendee_count = 0
                for row in reader:
                    # We should have logic here to first see if the attendee
                    # already exists and if they do, just add them to the
                    # course
                    attendee = Attendee(
                        firstname=row[0],
                        surname=row[1],
                        email=row[2],
                        certifying_organisation=self.certifying_organisation,
                        author=self.request.user,
                    )
                    try:
                        attendee.save()
                        attendee_count += 1
                    except:
                        #  Could not save - probably they exist already
                        attendee = None

                    if not attendee:
                        # put more checks in case attendee
                        # does not already exist
                        continue

                    course_attendee = CourseAttendee(
                        attendee=attendee,
                        course=course,
                        author=self.request.user,
                    )
                    try:
                        course_attendee.save()
                        course_attendee_count += 1
                    except:
                        #  They are probably already associated with a course
                        pass

                self.form_valid_message = (
                    '%i new attendees were created, and %i attendees were '
                    'added to the course: % s' % (
                        attendee_count, course_attendee_count, self.course)
                )

                self.form_invalid_message = (
                    'Something wrong happened while running the upload. '
                    'Please contact site support to help resolving the issue.')
            return self.form_valid(form)

        else:
            return self.form_invalid(form)
