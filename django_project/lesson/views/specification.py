# coding=utf-8
"""Specification views."""

from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.http import Http404
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from base.models.project import Project
from lesson.models.section import Section
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
    template_name = 'specification/create.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
            SpecificationCreateView, self).get_context_data(**kwargs)
        context['specification'] = Specification.objects.filter(
            worksheet=self.worksheet)
        context['worksheet'] = self.worksheet
        return context

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
        self.worksheet_slug = self.kwargs.get('worksheet_slug', None)
        self.worksheet = Worksheet.objects.get(slug=self.worksheet_slug)
        kwargs.update({
            # 'user': self.request.user,
            'worksheet': self.worksheet
        })
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            result = super(SpecificationCreateView, self).form_valid(form)
            return result
        except IntegrityError:
            raise ValidationError(
                'ERROR: Specification by this name already exists!')


# noinspection PyAttributeOutsideInit
class SpecificationDeleteView(
        LoginRequiredMixin,
        SpecificationMixin,
        DeleteView):
    """Delete view for Specification."""

    context_object_name = 'specification'
    template_name = 'specification/delete.html'

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
            SpecificationDeleteView, self).get(request, *args, **kwargs)

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
            SpecificationDeleteView, self).post(request, *args, **kwargs)

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
        qs = Specification.objects.filter(pk=self.pk)
        return qs


# noinspection PyAttributeOutsideInit
class SpecificationUpdateView(
        LoginRequiredMixin,
        SpecificationMixin,
        UpdateView):
    """Update view for Specification."""

    context_object_name = 'specification'
    template_name = 'specification/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            SpecificationUpdateView, self).get_form_kwargs()
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
            SpecificationUpdateView, self).get_context_data(**kwargs)
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
            queryset = Specification.objects.all()
        else:
            queryset = Specification.objects.filter(
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

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""

        try:
            return super(
                SpecificationUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Specification by this name is already exists!')


class SpecificationOrderView(
    SpecificationMixin, StaffuserRequiredMixin, ListView):
    """List view to order specifications"""
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
        context['num_specifications'] = context['specifications'].count()
        project_slug = self.kwargs.get('project_slug', None)
        section_slug = self.kwargs.get('section_slug', None)
        worksheet_slug = self.kwargs.get('worksheet_slug', None)
        if project_slug and section_slug and worksheet_slug:
            context['project'] = Project.objects.get(slug=project_slug)
            context['section'] = Section.objects.get(slug=section_slug)
            context['worksheet'] = Worksheet.objects.get(
                slug=worksheet_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved
            Categories.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            worksheet_slug = self.kwargs.get('worksheet_slug', None)
            if worksheet_slug:
                try:
                    worksheet = Worksheet.objects.get(slug=worksheet_slug)
                except Worksheet.DoesNotExist:
                    raise Http404(
                        'Sorry! The worksheet you are requesting a '
                        'specification for could not be found or you do not '
                        'have permission to view the specification.')
                queryset = Specification.objects.filter(worksheet=worksheet)
                return queryset
            else:
                raise Http404(
                        'Sorry! We could not find the worksheet for '
                        'your specification!')
        else:
            return queryset


class SpecificationOrderSubmitView(
    LoginRequiredMixin, SpecificationMixin, UpdateView):
    """Update order view for Specification"""
    context_object_name = 'specification'

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
