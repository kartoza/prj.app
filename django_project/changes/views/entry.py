# -*- coding: utf-8 -*-
"""View classes for Entry"""

from base.models import Project
# noinspection PyUnresolvedReferences
import logging
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView,
)
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin
from ..models import Version, Entry
from ..forms import EntryForm

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


class EntryListView(EntryMixin, PaginationMixin, ListView):
    """List view for Entry."""
    context_object_name = 'entries'
    template_name = 'entry/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(EntryListView, self).get_context_data(**kwargs)
        context['num_entries'] = self.get_queryset().count()
        context['unapproved'] = False
        context['project_slug'] = self.project_slug
        context['version_slug'] = self.version_slug
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Entry.
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            self.version_slug = self.kwargs.get('version_slug', None)
            if self.project_slug and self.version_slug:
                try:
                    project = Project.objects.get(slug=self.project_slug)
                except:
                    raise Http404('Project not found')
                try:
                    version = Version.objects.get(
                        slug=self.version_slug, project=project)
                except:
                    raise Http404('Version not found')
                queryset = Entry.objects.filter(version=version)
                return queryset
            else:
                raise Http404('Sorry! We could not find your entry!')
        return self.queryset


class EntryDetailView(EntryMixin, DetailView):
    """Detail view for Entry."""
    context_object_name = 'entry'
    template_name = 'entry/detail.html'

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Entry slugs are unique within a Version, we need to make
        sure that we fetch the correct Entry from the correct Version

        :param queryset
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show an Entry
        :rtype QuerySet
        :raises: Http404
        """
        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            version_slug = self.kwargs.get('version_slug', None)
            if slug and project_slug and version_slug:
                try:
                    project = Project.objects.get(slug=project_slug)
                except:
                    raise Http404('Project could not be found')
                try:
                    version = Version.objects.get(
                        slug=version_slug, project=project)
                except:
                    raise Http404('Version could not be found')
                try:
                    obj = queryset.get(slug=slug, version=version)
                except:
                    raise Http404('Change could not be found')
                return obj
            else:
                raise Http404('Sorry! We could not find your entry!')


# noinspection PyAttributeOutsideInit
class EntryDeleteView(LoginRequiredMixin, EntryMixin, DeleteView):
    """Delete view for Entry."""
    context_object_name = 'entry'
    template_name = 'entry/delete.html'

    def get(self, request, *args, **kwargs):
        """Access URL parameters

        We need to define self.project and self.version

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.entry_id = self.kwargs.get('pk', None)
        self.entry_id = Entry.objects.get(id=self.entry_id)
        return super(EntryDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Access URL parameters

        We need to define self.project and self.version

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.entry_id = self.kwargs.get('pk', None)
        self.entry = Entry.objects.get(id=self.entry_id)
        return super(EntryDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion of the object, the User will be redirected
        to the Entry list page for the object's parent Version and Project

        :return: URL
        :rtype: HttpResponse
        """
        return reverse('entry-list', kwargs={
            'project_slug': self.object.version.project.slug,
            'version_slug': self.object.version.slug
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
        if not self.request.user.is_authenticated():
            raise Http404
        qs = Entry.objects
        # In future we should further filter to only allow deletion for
        # staff members when they are owners of the project...
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(author=self.request.user)


# noinspection PyAttributeOutsideInit
class EntryCreateView(LoginRequiredMixin, EntryMixin, CreateView):
    """Create view for Entry."""
    context_object_name = 'entry'
    template_name = 'entry/create.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(EntryCreateView, self).get_context_data(**kwargs)
        context['entries'] = self.get_queryset()\
            .filter(version=self.version)
        return context

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the Entry list page for the object's parent Version and Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('pending-entry-list', kwargs={
            'project_slug': self.object.version.project.slug,
            'version_slug': self.object.version.slug
        })

    def form_valid(self, form):
        """Save new created Entry

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect
        """
        """Check that there is no referential integrity error when saving."""
        try:
            super(EntryCreateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                'ERROR: Entry by this name already exists!')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        self.version_slug = self.kwargs.get('version_slug', None)
        self.version = Version.objects.get(slug=self.version_slug)
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'version': self.version,
            'project': self.project
        })
        return kwargs


# noinspection PyAttributeOutsideInit
class EntryUpdateView(LoginRequiredMixin, EntryMixin, UpdateView):
    """Update view for Entry."""
    context_object_name = 'entry'
    template_name = 'entry/update.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(EntryUpdateView, self).get_context_data(**kwargs)
        context['entries'] = Entry.objects.filter(version=self.version)
        return context

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
        self.entry = Entry.objects.get(id=entry_id)
        self.version = self.entry.version
        self.project = self.version.project

        kwargs.update({
            'user': self.request.user,
            'instance': self.entry,
            'version': self.version,
            'project': self.project
        })
        return kwargs

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the Entry list page for the object's parent Version and Project

        :return: URL
        :rtype: HttpResponse
        """
        return reverse('pending-entry-list', kwargs={
            'project_slug': self.object.version.project.slug,
            'version_slug': self.object.version.slug}
        )

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(EntryUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Entry by this name already exists!')


# noinspection PyAttributeOutsideInit
class PendingEntryListView(EntryMixin, PaginationMixin, ListView,
                           StaffuserRequiredMixin):
    """List view for pending Entry."""
    context_object_name = 'unapproved_entries'
    template_name = 'entry/pending-list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(PendingEntryListView, self).get_context_data(**kwargs)
        context['num_entries'] = self.get_queryset().count()
        context['unapproved'] = True
        context['entries'] = Entry.objects.filter(version=self.version)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

         :returns: A queryset which is filtered to only show unapproved
            Entry.
         :rtype: QuerySet
         :raises: Http404
         """
        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            version_slug = self.kwargs.get('version_slug', None)
            if project_slug and version_slug:
                try:
                    project = Project.objects.get(slug=project_slug)
                except:
                    raise Http404('Project not found')
                try:
                    self.version = Version.objects.get(
                        slug=version_slug, project=project)
                except:
                    raise Http404('Version not found')
                queryset = Entry.unapproved_objects.filter(
                    version=self.version)
                if self.request.user.is_staff:
                    return queryset
                else:
                    try:
                        return queryset.filter(author=self.request.user)
                    except:
                        raise Http404('Sorry! We could not find your entry!')
            else:
                raise Http404('Sorry! We could not find your entry!')
        return self.queryset


class ApproveEntryView(StaffuserRequiredMixin, EntryMixin, RedirectView):
    """View for approving Entry."""
    permanent = False
    query_string = True
    pattern_name = 'entry-list'

    def get_redirect_url(self, pk):
        """Save Version as approved and redirect

        :param pk: The primary key of the Entry
        :type pk: str

        :returns: URL
        :rtype: str
        """
        entry_qs = Entry.unapproved_objects
        entry = get_object_or_404(entry_qs, id=pk)
        entry.approved = True
        entry.save()
        # Using Entry.version.project.slug instead of project_slug to ensure
        # that we redirect to the correct URL instead of relying on inputs from
        # URL.
        return reverse(self.pattern_name, kwargs={
            'project_slug': entry.version.project.slug,
            'version_slug': entry.version.slug
        })
