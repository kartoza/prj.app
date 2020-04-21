# coding=utf-8
"""Specification views."""

from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from lesson.models.specification import Specification
from lesson.models.worksheet import Worksheet
from lesson.forms.specification import SpecificationForm
from lesson.utilities import re_order_features


class SpecificationMixin(object):
    """Mixin class to provide standard settings for Specification."""

    model = Specification
    form_class = SpecificationForm


class SpecificationCreateView(
    LoginRequiredMixin, SpecificationMixin, CreateView):
    """Create view for Specification."""

    context_object_name = 'specification'
    template_name = 'create.html'
    creation_label = _('Add specification')

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Version list page for the object's parent Worksheet

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
        kwargs = super(SpecificationCreateView, self).get_form_kwargs()
        worksheet_slug = self.kwargs['worksheet_slug']
        kwargs['worksheet'] = get_object_or_404(Worksheet, slug=worksheet_slug)
        return kwargs


# noinspection PyAttributeOutsideInit
class SpecificationDeleteView(
        LoginRequiredMixin,
        SpecificationMixin,
        DeleteView):
    """Delete view for Specification."""

    context_object_name = 'specification'
    template_name = 'specification/delete.html'

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


# noinspection PyAttributeOutsideInit
class SpecificationUpdateView(
        LoginRequiredMixin,
        SpecificationMixin,
        UpdateView):
    """Update view for Specification."""

    context_object_name = 'specification'
    template_name = 'update.html'
    update_label = _('Update specification')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SpecificationUpdateView, self).get_form_kwargs()
        worksheet_slug = self.kwargs.get('worksheet_slug', None)
        kwargs['worksheet'] = get_object_or_404(Worksheet, slug=worksheet_slug)
        return kwargs

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


class SpecificationOrderView(
    LoginRequiredMixin, SpecificationMixin, ListView):
    """List view to order specifications."""
    context_object_name = 'specifications'
    template_name = 'specification/order.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
            SpecificationOrderView, self).get_context_data(**kwargs)
        worksheet_slug = self.kwargs.get('worksheet_slug', None)
        context['worksheet'] = get_object_or_404(
            Worksheet, slug=worksheet_slug)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only specifications.

        :rtype: QuerySet
        :raises: Http404
        """
        worksheet_slug = self.kwargs.get('worksheet_slug', None)
        worksheet = get_object_or_404(Worksheet, slug=worksheet_slug)
        queryset = Specification.objects.filter(worksheet=worksheet)
        return queryset


class SpecificationOrderSubmitView(
    LoginRequiredMixin, SpecificationMixin, UpdateView):
    """Update order view for Specification."""

    def post(self, request, *args, **kwargs):
        """Post the worksheet_slug from the URL and define the Worksheet

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        :raises: Http404
        """
        worksheet = Worksheet.objects.get(slug=kwargs.get('worksheet_slug'))
        specifications = Specification.objects.filter(worksheet=worksheet)
        return re_order_features(request, specifications)
