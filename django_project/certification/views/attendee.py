# coding=utf-8
import csv

from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView, FormView)
from braces.views import LoginRequiredMixin
from ..models import Attendee, CertifyingOrganisation
from ..forms import AttendeeForm


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

from ..forms import CsvAttendeeForm


class CsvUploadView(FormView):
    """
    Import Attendee CSV file into Attendee Model.
    """

    template_name = \
        'attendee/upload_attendee_csv.html'
    form_class = CsvAttendeeForm
    success_url = '/thanks/'

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handles POST requests, instantiating a form instance with the passed
    #     POST variables and then checked for validity.
    #     """
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    def form_valid(self, form):
        filename = CsvAttendeeForm(self.request.POST, self.request.FILES['file'])
        if self.request.method == "POST":
            # form = CsvAttendeeForm(self.request.POST, self.request.FILES)
            # filename = self.request.get('file').open('rb')
            # filename = (self.request.FILES['file'])
            with open(filename, 'rb') as f:
                reader = csv.reader(f, delimiter=',')
                next(reader)
                Attendee.objects.bulk_create([Attendee(
                        firstname=row[0],
                        surname=row[1],
                        email=row[2]
                    )for row in reader])
                # attendee_model = Attendee.objects.bulk_create(
                #     firstname=self.get_form_kwargs().get('file')['firstname'],
                #     surname = self.get_form_kwargs().get('file')['surname'],
                #     email = self.get_form_kwargs().get('file')['email'])
                Attendee.save()
                self.id = Attendee.id()


from django.shortcuts import render,redirect
def csv_upload(request, project_slug, organisation_slug, slug):

    if request.method == 'POST':
        form = CsvAttendeeForm(request.POST, request.FILES)
        if form.is_valid():
            # c = form.save(commit=False)
            form.author = request.user
            form.file = request.FILES
            import csv

            with open(form.file, 'rb') as f:
                reader = csv.reader(f, delimiter=',')
                next(reader)
                Attendee.objects.bulk_create(
                    [Attendee(firstname=row[0],
                              surname=row[1],
                              email=row[2])
                     for row in reader(form)])
                Attendee.save()
                request.id = Attendee.id()


            return redirect('/')
        else:
            template = 'attendee/upload_attendee_csv.html'

            render(request, template, {'form': form})

    else:
        form = CsvAttendeeForm()

    template = 'attendee/upload_attendee_csv.html'
    context = {
        'form': form
    }

    return render(request, template, context)

# class AttendeeCsvUploadMixin(object):
#     model = Attendee
#     form_class = CsvAttendeeForm
#
#
# class CsvUploadView(LoginRequiredMixin,
#                     AttendeeCsvUploadMixin,
#                     CreateView):