# coding=utf-8
import csv
from django.db import transaction
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    CreateView, FormView)
from braces.views import LoginRequiredMixin
from ..models import Attendee, CertifyingOrganisation
from ..forms import AttendeeForm
from ..forms import CsvAttendeeForm


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


class CsvUploadView(LoginRequiredMixin, FormView):
    """
    Allow upload of attendees
    through CSV file.
    """
    form_class = CsvAttendeeForm
    template_name = 'attendee/upload_attendee_csv.html'
    success_url = reverse_lazy('home')

    # @transaction.atomic()
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
                    [Attendee(firstname=row[0],
                              surname=row[1],
                              email=row[2],
                              )
                     for row in reader])

            return self.form_valid(form)

        else:
            return self.form_invalid(form)
