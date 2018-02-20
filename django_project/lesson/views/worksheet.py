# coding=utf-8
"""Worksheet views."""

from collections import OrderedDict
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from weasyprint import HTML

from lesson.forms.worksheet import WorksheetForm
from lesson.models.answer import Answer
from lesson.models.further_reading import FurtherReading
from lesson.models.section import Section
from lesson.models.specification import Specification
from lesson.models.worksheet import Worksheet
from lesson.models.worksheet_question import WorksheetQuestion
from lesson.utilities import re_order_features


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

        # Permissions
        context['user_can_edit'] = False
        lesson_managers = (
            context['worksheet'].section.project.lesson_managers.all())
        if self.request.user in lesson_managers:
            context['user_can_edit'] = True

        if self.request.user == context['worksheet'].section.project.owner:
            context['user_can_edit'] = True

        if self.request.user.is_staff:
            context['user_can_edit'] = True
        return context


class WorksheetPrintView(WorksheetDetailView):
    """Based on the WorkSheet Detail View, this is one is used for printing.

    If you want to render as HTML for debugging, you can simply comment the
    render_to_response method.
    """

    template_name = 'worksheet/print.html'

    def get(self, request, *args, **kwargs):
        host = request.get_host()
        if host == '0.0.0.0:61202':
            # We are using the dev environment with docker
            self.base_url = 'http://0.0.0.0:8080/'
        else:
            # On staging, host = staging.changelog.qgis.org
            self.base_url = request.scheme + host
        return super(WorksheetPrintView, self).get(request, args, kwargs)

    def render_to_response(self, context, **response_kwargs):
        response = super(WorksheetPrintView, self).render_to_response(
            context, **response_kwargs)
        response.render()
        pdf_response = HttpResponse(content_type='application/pdf')

        # Need to improve for URL outside of the dev env.
        html_object = HTML(
            string=response.content,
            base_url=self.base_url,
        )
        html_object.write_pdf(pdf_response)
        return pdf_response


class WorksheetCreateView(LoginRequiredMixin, WorksheetMixin, CreateView):
    """Create view for Section."""

    context_object_name = 'worksheet'
    template_name = 'create.html'
    creation_label = _('Add worksheet')

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
        section_slug = self.kwargs['section_slug']
        kwargs['section'] = get_object_or_404(Section, slug=section_slug)
        return kwargs


class WorksheetUpdateView(LoginRequiredMixin, WorksheetMixin, UpdateView):
    """Update view for worksheet."""

    context_object_name = 'worksheet'
    template_name = 'update.html'
    update_label = _('Update worksheet')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(WorksheetUpdateView, self).get_form_kwargs()
        slug = self.kwargs.get('section_slug', None)
        kwargs['section'] = get_object_or_404(Section, slug=slug)
        return kwargs

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


class WorksheetDeleteView(
        LoginRequiredMixin,
        WorksheetMixin,
        DeleteView):
    """Delete view for worksheet."""

    context_object_name = 'worksheet'
    template_name = 'worksheet/delete.html'

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


class WorksheetOrderView(StaffuserRequiredMixin, WorksheetMixin, ListView):
    """List view to order worksheet."""
    context_object_name = 'worksheets'
    template_name = 'worksheet/order.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(WorksheetOrderView, self).get_context_data(**kwargs)
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
    """Update order view for Worksheet."""

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
        section = Section.objects.get(slug=kwargs.get('section_slug'))
        worksheets = Worksheet.objects.filter(section=section)
        return re_order_features(request, worksheets)
