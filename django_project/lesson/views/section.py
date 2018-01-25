# coding=utf-8
"""Section views."""

from collections import OrderedDict

from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.http import Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin

from base.models.project import Project
from lesson.models.section import Section
from lesson.models.worksheet import Worksheet
from lesson.forms.section import SectionForm
from lesson.utilities import re_order_features


class SectionMixin(object):
    """Mixin class to provide standard settings for Section."""

    model = Section
    form_class = SectionForm


class SectionCreateView(LoginRequiredMixin, SectionMixin, CreateView):
    """Create view for Section."""

    context_object_name = 'section'
    template_name = 'create.html'
    creation_label = _('Add section')

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Version list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        url = '{url}#{anchor}'.format(
            url=reverse(
                'section-list',
                kwargs={'project_slug': self.object.project.slug}),
            anchor=self.object.slug
        )
        return url

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(SectionCreateView, self).get_form_kwargs()
        project_slug = self.kwargs['project_slug']
        kwargs['project'] = get_object_or_404(Project, slug=project_slug)
        return kwargs


class SectionListView(SectionMixin, PaginationMixin, ListView):
    """List view for Section."""

    context_object_name = 'sections'
    template_name = 'section/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SectionListView, self).get_context_data(**kwargs)
        context['project'] = get_object_or_404(
            Project, slug=self.kwargs.get('project_slug', None))
        context['worksheets'] = OrderedDict()
        for section in context['sections']:
            query_set = Worksheet.objects.filter(section=section)
            context['worksheets'][section] = query_set
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Version
        for this project.
        :rtype: QuerySet

        :raises: Http404
        """
        section_qs = Section.objects.all()
        project_slug = self.kwargs.get('project_slug', None)
        if project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
            except Project.DoesNotExist:
                raise Http404(
                    'The requested project does not exist.'
                )
            section_qs = section_qs.filter(project=project)
            return section_qs
        else:
            raise Http404('Sorry! We could not find your section!')


# noinspection PyAttributeOutsideInit
class SectionDeleteView(
        LoginRequiredMixin,
        SectionMixin,
        DeleteView):
    """Delete view for Section."""

    context_object_name = 'section'
    template_name = 'section/delete.html'

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

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(SectionDeleteView, self).get(request, *args, **kwargs)

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

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(SectionDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Section list page
        for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('section-list', kwargs={
            'project_slug': self.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the Section objects by
        Project before passing to get_object() to ensure that we
        return the correct Section object.
        The requesting User must be authenticated.

        :returns: Section queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated():
            raise Http404
        qs = Section.objects.filter(project=self.project)
        return qs


# noinspection PyAttributeOutsideInit
class SectionUpdateView(
        LoginRequiredMixin,
        SectionMixin,
        UpdateView):
    """Update view for Section."""

    context_object_name = 'section'
    template_name = 'section/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            SectionUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'project': self.project
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
            SectionUpdateView, self).get_context_data(**kwargs)
        context['section'] = self.get_queryset() \
            .filter(project=self.project)
        context['the_project'] = self.project
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        projects which user created (staff gets all projects)
        :rtype: QuerySet
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        if self.request.user.is_staff:
            queryset = Section.objects.all()
        else:
            queryset = Section.objects.filter(
                Q(project=self.project) &
                (Q(project__owner=self.request.user) |
                 Q(organisation_owners=self.request.user)))
        return queryset

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the section list page for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """
        url = '{url}#{anchor}'.format(
            url=reverse(
                'section-list',
                kwargs={'project_slug': self.object.project.slug}),
            anchor=self.object.slug
        )
        return url


class SectionOrderView(SectionMixin, StaffuserRequiredMixin, ListView):
    """List view to order section"""
    context_object_name = 'sections'
    template_name = 'section/order.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SectionOrderView, self).get_context_data(**kwargs)
        context['num_sections'] = context['sections'].count()
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
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
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                try:
                    project = Project.objects.get(slug=project_slug)
                except Project.DoesNotExist:
                    raise Http404(
                        'Sorry! The project you are requesting a section for '
                        'could not be found or you do not have permission to '
                        'view the section.')
                queryset = Section.objects.filter(project=project)
                return queryset
            else:
                raise Http404(
                        'Sorry! We could not find the project for '
                        'your section!')
        else:
            return queryset


class SectionOrderSubmitView(LoginRequiredMixin, SectionMixin, UpdateView):
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
        project = Project.objects.get(slug=kwargs.get('project_slug'))
        sections = Section.objects.filter(project=project)
        return re_order_features(request, sections)
