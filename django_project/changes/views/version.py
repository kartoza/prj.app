# coding=utf-8
"""Version related views."""
import logging
logger = logging.getLogger(__name__)

# noinspection PyUnresolvedReferences
import logging
logger = logging.getLogger(__name__)

from django.core.urlresolvers import reverse
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

from ..models import Project, Category, Version, Entry
from ..forms import ProjectForm, CategoryForm, VersionForm, EntryForm


class VersionMixin(object):
    """Mixing for all views to inherit which sets some standard properties."""
    model = Version  # implies -> queryset = Entry.objects.all()
    form_class = VersionForm


class VersionCreateUpdateMixin(VersionMixin, LoginRequiredMixin):
    """Mixin for views that do create or update operations."""
    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template."""
        context = super(VersionMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        """Behaviour for invalid forms.

        :param form: Form which is being validated.
        :type form: ModelForm
        """
        return self.render_to_response(self.get_context_data(form=form))


class VersionListView(VersionMixin, PaginationMixin, ListView):
    context_object_name = 'versions'
    template_name = 'version/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(VersionListView, self).get_context_data(**kwargs)
        context['num_versions'] = self.get_queryset().count()
        context['unapproved'] = False
        return context

    def get_queryset(self):
        versions_qs = Version.objects.all()
        return versions_qs


class VersionDetailView(VersionMixin, DetailView):
    """A tabular list style view for a version."""
    context_object_name = 'version'
    template_name = 'version/detail.html'

    def get_context_data(self, **kwargs):
        context = super(VersionDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        versions_qs = Version.objects.all()
        return versions_qs

    def get_object(self, queryset=None):
        obj = super(VersionDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class VersionMarkdownView(VersionDetailView):
    """Return a markdown version detail."""
    template_name = 'version/detail.md'

    def render_to_response(self, context, **response_kwargs):
        response = super(VersionMarkdownView, self).render_to_response(
            context,
            mimetype='application/text',
            **response_kwargs)
        response['Content-Disposition'] = 'attachment; filename="foo.md"'
        return response


class VersionThumbnailView(VersionMixin, DetailView):
    """A contact sheet style list of thumbs per entry."""
    context_object_name = 'version'
    template_name = 'version/detail-thumbs.html'

    def get_context_data(self, **kwargs):
        context = super(VersionThumbnailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        versions_qs = Version.objects.all()
        return versions_qs

    def get_object(self, queryset=None):
        obj = super(VersionThumbnailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class VersionDeleteView(VersionMixin, DeleteView, LoginRequiredMixin):
    context_object_name = 'version'
    template_name = 'version/delete.html'

    def get_success_url(self):
        return reverse('version-list')

    def get_queryset(self):
        qs = Version.all_objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)


class VersionCreateView(
        VersionCreateUpdateMixin, CreateView, LoginRequiredMixin):
    context_object_name = 'version'
    template_name = 'version/create.html'

    def get_success_url(self):
        return reverse('pending-version-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class VersionUpdateView(VersionCreateUpdateMixin, UpdateView):
    context_object_name = 'version'
    template_name = 'version/update.html'

    def get_form_kwargs(self):
        kwargs = super(VersionUpdateView, self).get_form_kwargs()
        return kwargs

    def get_queryset(self):
        versions_qs = Version.objects
        return versions_qs

    def get_success_url(self):
        return reverse('version-list')


class PendingVersionListView(
        VersionMixin, PaginationMixin, ListView, StaffuserRequiredMixin):
    """List all unapproved versions - staff see all """
    context_object_name = 'versions'
    template_name = 'version/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PendingVersionListView, self).get_context_data(**kwargs)
        context['num_versions'] = self.get_queryset().count()
        context['unapproved'] = True
        return context

    def get_queryset(self):
        versions_qs = Version.unapproved_objects.all()
        if self.request.user.is_staff:
            return versions_qs
        else:
            return versions_qs.filter(creator=self.request.user)


class ApproveVersionView(VersionMixin, StaffuserRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pending-version-list'

    def get_redirect_url(self, pk):
        version_qs = Version.unapproved_objects.all()
        version = get_object_or_404(version_qs, pk=pk)
        version.approved = True
        version.save()
        return reverse(self.pattern_name)
