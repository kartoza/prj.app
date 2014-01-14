import logging
from base.models import Project

logger = logging.getLogger(__name__)

# noinspection PyUnresolvedReferences
import logging
logger = logging.getLogger(__name__)

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
    TemplateView)

from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin

from ..models import Category, Version, Entry
from ..forms import CategoryForm, VersionForm, EntryForm


class EntryMixin(object):
    model = Entry  # implies -> queryset = Entry.objects.all()
    form_class = EntryForm


class EntryListView(EntryMixin, PaginationMixin, ListView):
    context_object_name = 'entries'
    template_name = 'entry/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        context['num_entries'] = self.get_queryset().count()
        context['unapproved'] = False
        return context

    def get_queryset(self):
        """Only approved objects are shown."""
        qs = Entry.approved_objects.all()
        return qs

    def get_object(self, queryset=None):
        """
        Get the object for this view.
        Because Entry slugs are unique within a Version, we need to make
        sure that we fetch the correct Entry from the correct Version
        """
        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            version_slug = self.kwargs.get('version_slug', None)
            if slug and project_slug and version_slug:
                project = Project.objects.get(slug=project_slug)
                version = Version.objects.get(slug=version_slug,
                                              project=project)
                obj = queryset.get(slug=slug, version=version)
                return obj
            else:
                raise Http404('Sorry! We could not find your entry!')


class EntryDetailView(EntryMixin, DetailView):
    context_object_name = 'entry'
    template_name = 'entry/detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Anyone can see any entry."""
        qs = Entry.objects.all()
        return qs

    def get_object(self, queryset=None):
        obj = super(EntryDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class EntryDeleteView(LoginRequiredMixin, EntryMixin, DeleteView):
    context_object_name = 'entry'
    template_name = 'entry/delete.html'

    def get_success_url(self):
        return reverse('entry-list', kwargs={
            'project_slug': self.object.version.project.slug,
            'version_slug': self.object.version.slug
        })

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise Http404
        qs = Entry.objects.all()

        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)


class EntryCreateView(LoginRequiredMixin, EntryMixin, CreateView):
    context_object_name = 'entry'
    template_name = 'entry/create.html'

    def get_success_url(self):
        return reverse('pending-entry-list', kwargs={
            'project_slug': self.object.version.project.slug,
            'version_slug': self.object.version.slug
        })

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EntryUpdateView(LoginRequiredMixin, EntryMixin, UpdateView):
    context_object_name = 'entry'
    template_name = 'entry/update.html'

    def get_form_kwargs(self):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        return kwargs

    def get_queryset(self):
        qs = Entry.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)

    def get_success_url(self):
        return reverse('pending-entry-list', kwargs={
            'project_slug': self.object.version.project.slug,
            'version_slug': self.object.version.slug
        })


class PendingEntryListView(EntryMixin,
                           PaginationMixin,
                           ListView,
                           StaffuserRequiredMixin):
    """List all unapproved entries"""
    context_object_name = 'entries'
    template_name = 'entry/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PendingEntryListView, self).get_context_data(**kwargs)
        context['num_entries'] = self.get_queryset().count()
        context['unapproved'] = True
        return context

    def get_queryset(self):
        qs = Entry.unapproved_objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)


class ApproveEntryView(StaffuserRequiredMixin, EntryMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pending-entry-list'

    def get_redirect_url(self, version_slug, project_slug, slug):
        entry_qs = Entry.unapproved_objects.all()
        entry = get_object_or_404(entry_qs, slug=slug)
        entry.approved = True
        entry.save()
        # Using entry.version.project.slug instead of project_slug to ensure
        # that we redirect to the correct URL instead of relying on inputs from
        # URL.
        return reverse(self.pattern_name, kwargs={
            'project_slug': entry.version.project.slug,
            'version_slug': entry.version.slug
        })
