# coding=utf-8
"""Worksheet views."""

from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http import Http404
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin

from base.models.project import Project
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

        context['requirements'] = Specification.objects.filter(
            worksheet=pk).order_by('specification_number')

        questions = WorksheetQuestion.objects.filter(
            worksheet=pk).order_by('question_number')
        context['questions'] = {}
        for question in questions:
            context['questions'][question] = Answer.objects.filter(
                question=question).order_by('answer_number')

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
        return reverse('worksheet-list', kwargs={
            'section_slug': self.object.section.slug,
            'project_slug': self.object.section.project.slug,
        })

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


class WorksheetListView(WorksheetMixin, PaginationMixin, ListView):
    """List view for Worksheet."""

    context_object_name = 'worksheets'
    template_name = 'worksheet/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(WorksheetListView, self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        section_slug = self.kwargs.get('section_slug', None)
        if project_slug and section_slug:
            context['project'] = Project.objects.get(slug=project_slug)
            context['section'] = Section.objects.get(slug=section_slug)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Version
        for this project.
        :rtype: QuerySet

        :raises: Http404
        """
        worksheet_qs = Worksheet.objects.all()
        section_slug = self.kwargs.get('section_slug', None)
        if section_slug:
            section = get_object_or_404(Section, slug=section_slug)
            worksheet_qs = worksheet_qs.filter(
                section=section).order_by('-module')
            return worksheet_qs
        else:
            raise Http404('Sorry! We could not find your section!')
