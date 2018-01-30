# coding=utf-8
"""Further reading views."""

from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
)
from django.http import Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from lesson.models.further_reading import FurtherReading
from lesson.models.worksheet import Worksheet
from lesson.forms.further_reading import FurtherReadingForm


class FurtherReadingMixin(object):
    """Mixin class to provide standard settings for Further Reading."""

    model = FurtherReading
    form_class = FurtherReadingForm


class FurtherReadingCreateView(
    LoginRequiredMixin, FurtherReadingMixin, CreateView):
    """Create view for Further Reading."""

    context_object_name = 'further_reading'
    template_name = 'create.html'
    creation_label = _('Add further reading item')

    def get_success_url(self):
        """Define the redirect URL

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.worksheet.pk,
            'section_slug': self.object.worksheet.section.slug,
            'project_slug': self.object.worksheet.section.project.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(FurtherReadingCreateView, self).get_form_kwargs()
        worksheet_slug = self.kwargs['worksheet_slug']
        kwargs['worksheet'] = get_object_or_404(Worksheet, slug=worksheet_slug)
        return kwargs


# noinspection PyAttributeOutsideInit
class FurtherReadingDeleteView(
        LoginRequiredMixin,
        FurtherReadingMixin,
        DeleteView):
    """Delete view for Further reading."""

    context_object_name = 'further_reading'
    template_name = 'further_reading/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the worksheet_slug from the URL and define the Worksheet.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.pk = self.kwargs.get('pk', None)
        return super(
            FurtherReadingDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the worksheet_slug from the URL and define the Worksheet.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.pk = self.kwargs.get('pk', None)
        return super(
            FurtherReadingDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation list page
        for the object's parent Worksheet.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('worksheet-detail', kwargs={
            'pk': self.object.worksheet.pk,
            'section_slug': self.object.worksheet.section.slug,
            'project_slug': self.object.worksheet.section.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the CertifyingOrganisation objects by
        Worksheet before passing to get_object() to ensure that we
        return the correct Certifying Organisation object.
        The requesting User must be authenticated.

        :returns: Certifying Organisation queryset filtered by Worksheet
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated():
            raise Http404
        qs = FurtherReading.objects.filter(pk=self.pk)
        return qs


# noinspection PyAttributeOutsideInit
class FurtherReadingUpdateView(
        LoginRequiredMixin,
        FurtherReadingMixin,
        UpdateView):
    """Update view for Further Reading."""

    context_object_name = 'further_reading'
    template_name = 'further_reading/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            FurtherReadingUpdateView, self).get_form_kwargs()
        self.worksheet_slug = self.kwargs.get('worksheet_slug', None)
        self.worksheet = Worksheet.objects.get(slug=self.worksheet_slug)
        kwargs.update({
            'worksheet': self.worksheet
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            FurtherReadingUpdateView, self).get_context_data(**kwargs)
        context['specification'] = self.get_queryset() \
            .filter(worksheet=self.worksheet)
        context['the_worksheet'] = self.worksheet
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        worksheets which user created (staff gets all worksheets)
        :rtype: QuerySet
        """

        self.worksheet_slug = self.kwargs.get('worksheet_slug', None)
        self.worksheet = Worksheet.objects.get(slug=self.worksheet_slug)
        if self.request.user.is_staff:
            queryset = FurtherReading.objects.all()
        else:
            queryset = FurtherReading.objects.filter(
                Q(worksheet=self.worksheet) &
                (Q(worksheet__owner=self.request.user) |
                 Q(organisation_owners=self.request.user)))
        return queryset

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the specification list page for the object's parent Worksheet.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('worksheet-detail', kwargs={
            'pk': self.object.worksheet.pk,
            'section_slug': self.object.worksheet.section.slug,
            'project_slug': self.object.worksheet.section.project.slug
        })
