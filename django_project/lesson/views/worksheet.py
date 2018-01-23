# coding=utf-8
"""Worksheet views."""

import json

from collections import OrderedDict
from django.core.urlresolvers import reverse
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from lesson.forms.worksheet import WorksheetForm
from lesson.models.answer import Answer
from lesson.models.further_reading import FurtherReading
from lesson.models.section import Section
from lesson.models.specification import Specification
from lesson.models.worksheet import Worksheet
from lesson.models.worksheet_question import WorksheetQuestion


class WorksheetMixin(object):
    """Mixin class to provide standard settings for Worksheet."""

    model = Worksheet
    form_class = WorksheetForm


class WorksheetDetailView(
        WorksheetMixin,
        DetailView):
    """Detail view for worksheet."""

    context_object_name = 'worksheet'
    template_name = 'worksheet/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(WorksheetDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)

        context['requirements'] = Specification.objects.filter(worksheet=pk)

        questions = WorksheetQuestion.objects.filter(worksheet=pk)
        context['questions'] = OrderedDict()
        for question in questions:
            context['questions'][question] = Answer.objects.filter(
                question=question)

        context['further_reading'] = FurtherReading.objects.filter(
            worksheet=pk)

        return context


class WorksheetCreateView(LoginRequiredMixin, WorksheetMixin, CreateView):
    """Create view for Section."""

    context_object_name = 'worksheet'
    template_name = 'worksheet/create.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(WorksheetCreateView, self).get_context_data(**kwargs)
        context['section'] = self.section
        return context

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Version list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.pk,
            'section_slug': self.object.section.slug,
            'project_slug': self.object.section.project.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(WorksheetCreateView, self).get_form_kwargs()
        self.section = Section.objects.get(
            slug=self.kwargs.get('section_slug', None))
        kwargs.update({
            'section': self.section,
        })
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            result = super(WorksheetCreateView, self).form_valid(form)
            return result
        except IntegrityError:
            raise ValidationError(
                'ERROR: Worksheet by this name already exists!')


class WorksheetUpdateView(LoginRequiredMixin, WorksheetMixin, UpdateView):
    """Update view for worksheet."""

    context_object_name = 'worksheet'
    template_name = 'worksheet/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(WorksheetUpdateView, self).get_form_kwargs()
        self.section = Section.objects.get(
            slug=self.kwargs.get('section_slug', None))
        kwargs.update({
            'section': self.section
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(WorksheetUpdateView, self).get_context_data(**kwargs)
        context['section'] = self.section
        return context

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the section detail (worksheet list) page.

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.pk,
            'project_slug': self.object.section.project.slug,
            'section_slug': self.object.section.slug,
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(WorksheetUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Worksheet is already existing!')


class WorksheetDeleteView(
        LoginRequiredMixin,
        WorksheetMixin,
        DeleteView):
    """Delete view for worksheet."""

    context_object_name = 'worksheet'
    template_name = 'worksheet/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project.

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
            WorksheetDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project.

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
            WorksheetDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the section detail (worksheet list) page
        for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """
        url = '{url}#{anchor}'.format(
            url=reverse(
                'section-list',
                kwargs={'project_slug': self.object.section.project.slug}),
            anchor=self.object.section.slug
        )
        return url

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the Worksheet objects by
        Project before passing to get_object() to ensure that we
        return the correct Worksheet object.
        The requesting User must be authenticated.

        :returns: Worksheet queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """
        if not self.request.user.is_authenticated():
            raise Http404
        qs = Worksheet.objects.filter(pk=self.pk)
        return qs


class WorksheetOrderView(WorksheetMixin, StaffuserRequiredMixin, ListView):
    """List view to order worksheet."""
    context_object_name = 'worksheet'
    template_name = 'worksheet/order.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(WorksheetOrderView, self).get_context_data(**kwargs)
        context['num_items'] = context['worksheet'].count()
        section_slug = self.kwargs.get('section_slug', None)
        context['section'] = Section.objects.get(slug=section_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved
            Categories.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        section_slug = self.kwargs.get('section_slug', None)
        section = get_object_or_404(Section, slug=section_slug)
        queryset = Worksheet.objects.filter(section=section)
        return queryset


class WorksheetOrderSubmitView(LoginRequiredMixin, WorksheetMixin, UpdateView):
    """Update order view for Section"""
    context_object_name = 'section'

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project

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
        section_slug = kwargs.get('section_slug')
        section = Section.objects.get(slug=section_slug)
        worksheets = Worksheet.objects.filter(section=section)
        worksheets_json = request.body

        try:
            worksheets_request = json.loads(worksheets_json)
        except ValueError:
            raise Http404('Error json values')

        # Add dummy shift in the DB to avoid Integrity about unique_together
        for worksheet in worksheets:
            worksheet.order_number += len(worksheets_request)
            worksheet.save()

        for worksheet_request in worksheets_request:
            worksheet = worksheets.get(id=worksheet_request['id'])
            if worksheet:
                worksheet.order_number = worksheet_request['sort_number']
                worksheet.save()

        return HttpResponse('')
