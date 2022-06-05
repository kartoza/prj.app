# coding=utf-8
import io
import csv
from datetime import timedelta, datetime

from django.db import transaction
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import (
    CreateView, FormView, UpdateView)
from braces.views import LoginRequiredMixin, FormMessagesMixin
from certification.models import (
    Attendee, CertifyingOrganisation, CourseAttendee, Course, Certificate
)
from certification.forms import (
    AttendeeForm, CsvAttendeeForm, UpdateAttendeeForm)


class AttendeeMixin(object):
    """Mixin class to provide standard settings for Attendee."""

    model = Attendee
    form_class = AttendeeForm


class AttendeeCreateView(LoginRequiredMixin, AttendeeMixin, CreateView):
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
        add_to_course = self.request.POST.get('add_to_course')
        if add_to_course is None:
            success_url = reverse('courseattendee-create', kwargs={
                'project_slug': self.project_slug,
                'organisation_slug': self.organisation_slug,
                'slug': self.course_slug,
            })
        else:
            success_url = reverse('course-detail', kwargs={
                'project_slug': self.project_slug,
                'organisation_slug': self.organisation_slug,
                'slug': self.course_slug,
            })
        return success_url

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

    def form_valid(self, form):
        add_to_course = self.request.POST.get('add_to_course')
        if add_to_course is None:
            if form.is_valid():
                form.save()
        else:
            if form.is_valid():
                object = form.save()
                course_slug = self.kwargs.get('slug', None)
                course = Course.objects.get(slug=course_slug)
                course_attendee = CourseAttendee(
                    attendee=object,
                    course=course,
                    author=self.request.user
                )
                course_attendee.save()
        return super(AttendeeCreateView, self).form_valid(form)


class CsvUploadView(FormMessagesMixin, LoginRequiredMixin, FormView):
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
        return kwargs

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """Get form instance from upload.

           After successful creation of the object,the User
           will be redirected to the create course attendee page.

          :returns: URL
          :rtype: HttpResponse
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        attendees_file = request.FILES.get('file')
        attendees_file.seek(0)
        course = Course.objects.get(slug=self.slug)
        if form.is_valid():
            if attendees_file:
                reader = csv.DictReader(
                    io.StringIO(attendees_file.read().decode('utf-8'))
                )
                fieldnames = reader.fieldnames
                attendee_count = 0
                course_attendee_count = 0
                existing_attendee_count = 0
                for row in reader:
                    # We should have logic here to first see if the attendee
                    # already exists and if they do, just add them to the
                    # course
                    try:
                        attendee = Attendee.objects.get(
                            firstname=row[fieldnames[0]],
                            surname=row[fieldnames[1]],
                            email=row[fieldnames[2]],
                            certifying_organisation=
                            self.certifying_organisation,
                        )
                    except Attendee.DoesNotExist:
                        attendee = Attendee(
                            firstname=row[fieldnames[0]],
                            surname=row[fieldnames[1]],
                            email=row[fieldnames[2]],
                            certifying_organisation=
                            self.certifying_organisation,
                            author=self.request.user
                        )
                        attendee.save()
                        attendee_count += 1

                    try:
                        course_attendee = CourseAttendee.objects.get(
                            attendee=attendee,
                            course=course,
                        )
                    except CourseAttendee.DoesNotExist:
                        course_attendee = CourseAttendee(
                            attendee=attendee,
                            course=course,
                            author=self.request.user
                        )
                        course_attendee.save()
                        course_attendee_count += 1
                    else:
                        existing_attendee_count += 1

                self.form_valid_message = (
                    'From the csv: {} attendee already exist in this course, '
                    '{} new attendees were created, and {} attendees were '
                    'added to the course: {}'.format(
                        existing_attendee_count,
                        attendee_count,
                        course_attendee_count,
                        self.course)
                )

                self.form_invalid_message = (
                    'Something wrong happened while running the upload. '
                    'Please contact site support to help resolving the issue.')
            return self.form_valid(form)

        else:
            return self.form_invalid(form)


class AttendeeUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating attendee."""

    context_object_name = 'attendee'
    template_name = 'attendee/update.html'
    model = Attendee
    form_class = UpdateAttendeeForm

    def get_success_url(self):
        """Define the redirect URL.

        After successful updating the object, the User will be redirected
        to the course detail page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('course-detail', kwargs={
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
            AttendeeUpdateView, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(AttendeeUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.course_slug = self.kwargs.get('course_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation
        })
        return kwargs

    def get(self, request, *args, **kwargs):
        self.course_slug = self.kwargs.get('course_slug', None)
        course = Course.objects.get(slug=self.course_slug)
        certificate = Certificate.objects.filter(
            course=course,
            attendee=self.get_object()
        ).first()
        if certificate:
            if (
                not certificate.issue_date or
                certificate.issue_date +
                    timedelta(days=7) <= datetime.today().date()
            ):
                return HttpResponseForbidden('Course is not editable.')
        return super(AttendeeUpdateView, self).get(request, *args, **kwargs)
