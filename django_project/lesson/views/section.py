# coding=utf-8
"""Section views."""

from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView)
from django.http import Http404
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
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
    template_name = ''

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
