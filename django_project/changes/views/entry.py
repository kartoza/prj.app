# -*- coding: utf-8 -*-
"""View classes for Entry."""

from base.models import Project
# noinspection PyUnresolvedReferences
import logging
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from braces.views import LoginRequiredMixin
from ..models import Version, Entry, Category
from ..forms import EntryForm
from lesson.utilities import re_order_features

logger = logging.getLogger(__name__)

__author__ = 'Tim Sutton <tim@linfinit.com>'
__revision__ = '$Format:%H$'
__date__ = ''
__license__ = ''
__copyright__ = ''


class EntryMixin(object):
    """Mixing for all views to inherit which sets some standard properties."""
    model = Entry  # implies -> queryset = Entry.objects.all()
    form_class = EntryForm


class EntryDetailView(EntryMixin, DetailView):
    """Detail view for Entry."""
    context_object_name = 'entry'
    template_name = 'entry/detail.html'


# noinspection PyAttributeOutsideInit
class EntryDeleteView(LoginRequiredMixin, EntryMixin, DeleteView):
    """Delete view for Entry."""
    context_object_name = 'entry'
    template_name = 'entry/delete.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion of the object, the User will be redirected
        to the Entry list page for the object's parent Version and Project

        :return: URL
        :rtype: HttpResponse
        """
        return reverse('version-detail', kwargs={
            'project_slug': self.object.version.project.slug,
            'slug': self.object.version.slug
        })

    def get_queryset(self):
        """Define the queryset for this view

        If the requesting User is not authenticated, raise Http404.
        If the requesting User is not staff, only return Entry objects
        which the User has authored.

        :returns: Entry queryset filtered by version and user
        :rtype: QuerySet
        :raises: Http404
        """
        qs = Entry.objects.filter(version__locked=False)
        # In future we should further filter to only allow deletion for
        # staff members when they are owners of the project...
        pk_entry = self.kwargs.get('pk', None)
        entry = Entry.objects.get(pk=pk_entry)
        project = entry.version.project
        if self.request.user.is_staff \
                or self.request.user == project.owner \
                or self.request.user in project.changelog_managers.all():
            return qs
        else:
            return qs.filter(author=self.request.user)


# noinspection PyAttributeOutsideInit
class EntryCreateView(LoginRequiredMixin, EntryMixin, CreateView):
    """Create view for Entry."""
    context_object_name = 'entry'
    template_name = 'entry/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Entry list page for the object's parent Version and Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('version-detail', kwargs={
            'project_slug': self.object.version.project.slug,
            'slug': self.object.version.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form.
        :rtype: dict
        """
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        version_slug = self.kwargs.get('version_slug', None)
        project_slug = self.kwargs.get('project_slug', None)
        project = get_object_or_404(Project, slug=project_slug)
        version = get_object_or_404(
            Version, slug=version_slug, project=project)

        kwargs['user'] = self.request.user
        kwargs['version'] = version
        kwargs['project'] = project
        return kwargs


# noinspection PyAttributeOutsideInit
class EntryUpdateView(LoginRequiredMixin, EntryMixin, UpdateView):
    """Update view for Entry."""
    context_object_name = 'entry'
    template_name = 'entry/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        .. note:: There is a unique_together constraint on entries so the
            only way to uniquely retrieve an entry is the permutation of its
            project, version, category and slug.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        entry_id = int(self.kwargs.get('pk', None))
        entry = Entry.objects.get(id=entry_id)
        version = entry.version
        project = version.project

        kwargs['user'] = self.request.user
        kwargs['instance'] = entry
        kwargs['version'] = version
        kwargs['project'] = project
        return kwargs

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the Entry list page for the object's parent Version and Project

        :return: URL
        :rtype: HttpResponse
        """
        return reverse('version-detail', kwargs={
            'project_slug': self.object.version.project.slug,
            'slug': self.object.version.slug}
        )

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which shows all Versions if user.is_staff,
                or only the creator's Versions if not user.is_staff.
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated:
            raise Http404
        qs = Entry.objects.filter(version__locked=False)
        return qs


class EntryOrderView(LoginRequiredMixin, EntryMixin, ListView):
    """List view to order entries."""
    template_name = 'entry/order.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(EntryOrderView, self).get_context_data(**kwargs)
        version_pk = self.kwargs.get('version_pk', None)
        category_pk = self.kwargs.get('category_pk', None)
        context['version'] = get_object_or_404(Version, pk=version_pk)
        context['category'] = get_object_or_404(Category, pk=category_pk)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show entries for this
        version and this category.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        version_pk = self.kwargs.get('version_pk', None)
        category_pk = self.kwargs.get('category_pk', None)
        version = get_object_or_404(Version, pk=version_pk)
        category = get_object_or_404(Category, pk=category_pk)
        queryset = Entry.objects.filter(version=version, category=category)
        return queryset


class EntryOrderSubmitView(LoginRequiredMixin, EntryMixin, UpdateView):
    """Update order view for Section."""

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
        version_pk = self.kwargs.get('version_pk', None)
        category_pk = self.kwargs.get('category_pk', None)
        version = get_object_or_404(Version, pk=version_pk)
        category = get_object_or_404(Category, pk=category_pk)
        queryset = Entry.objects.filter(version=version, category=category)
        return re_order_features(request, queryset)
