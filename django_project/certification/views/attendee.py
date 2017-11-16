# coding=utf-8
import csv
from django.db import transaction
from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView, FormView)
from braces.views import LoginRequiredMixin, FormMessagesMixin
from ..models import Attendee, CertifyingOrganisation
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
    Allow upload of attendees
    through CSV file.
    """
    context_object_name = 'courseattendee'

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
        file = request.FILES.get('file')
        if form.is_valid():
            if file:
                reader = csv.reader(file, delimiter=',')
                next(reader)
                Attendee.objects.bulk_create(
                    [Attendee(
                        firstname=row[0],
                        surname=row[1],
                        email=row[2],
                        certifying_organisation=self.certifying_organisation,
                        author=self.request.user,
                    ) for row in reader])

                self.form_valid_message = \
                    "3 Attendees were successfully added to the course : %s" % \
                    (self.course)
                self.form_invalid_message = \
                    "Something wrong happened while " \
                    "running the upload. Please try again."
            return self.form_valid(form)

        else:
            return self.form_invalid(form)
