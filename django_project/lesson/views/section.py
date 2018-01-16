# coding=utf-8
"""Section views."""

from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
)
from django.http import Http404
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from braces.views import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin

from base.models.project import Project
from lesson.models.section import Section
from lesson.forms.section import SectionForm


class SectionMixin(object):
    """Mixin class to provide standard settings for Section."""

    model = Section
    form_class = SectionForm


class SectionCreateView(LoginRequiredMixin, SectionMixin, CreateView):
    """Create view for Section."""

    context_object_name = 'section'
    template_name = 'section/create.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SectionCreateView, self).get_context_data(**kwargs)
        context['section'] = Section.objects.filter(project=self.project)
        context['project'] = self.project
        return context

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Version list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('section-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(SectionCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            # 'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            result = super(SectionCreateView, self).form_valid(form)
            return result
        except IntegrityError:
            raise ValidationError(
                'ERROR: Section by this name already exists!')


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
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
            context['project'] = context['the_project']
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
            section_qs = section_qs.filter(
                project=project).order_by('-section_number')
            return section_qs
        else:
            raise Http404('Sorry! We could not find your section!')


class SectionDetailView(SectionMixin, DetailView):
    """Detail view for Section."""

    context_object_name = 'section'
    template_name = 'section/detail.html'


    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SectionDetailView, self).get_context_data(**kwargs)

        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset for All Sections
        :rtype: QuerySet
        """

        qs = Section.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Certifying Organisation slugs are unique within a Project,
        we need to make sure that we fetch the correct
        Certifying Organisation from the correct Project

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a project
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            if slug and project_slug:
                project = Project.objects.get(slug=project_slug)
                obj = queryset.get(project=project, slug=slug)
                return obj
            else:
                raise Http404(
                    'Sorry! We could not find your Section!')


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
        to the Certifying Organisation list page
        for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('section-list', kwargs={
            'project_slug': self.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the CertifyingOrganisation objects by
        Project before passing to get_object() to ensure that we
        return the correct Certifying Organisation object.
        The requesting User must be authenticated.

        :returns: Certifying Organisation queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated():
            raise Http404
        qs = Section.objects.filter(project=self.project)
        return qs
