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

from ..models import Category, Version, Entry
from ..forms import CategoryForm, VersionForm, EntryForm


class EntryMixin(object):
    model = Entry  # implies -> queryset = Entry.objects.all()
    form_class = EntryForm


class EntryCreateUpdateMixin(EntryMixin, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(EntryMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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


class EntryDeleteView(EntryMixin, DeleteView, LoginRequiredMixin):
    context_object_name = 'entry'
    template_name = 'entry/delete.html'

    def get_success_url(self):
        return reverse('entry-list')

    def get_queryset(self):
        qs = Entry.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            qs.filter(creator=self.request.user)


class EntryCreateView(EntryCreateUpdateMixin, CreateView):
    context_object_name = 'entry'
    template_name = 'entry/create.html'

    def get_success_url(self):
        return reverse('pending-entry-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class EntryUpdateView(EntryCreateUpdateMixin, UpdateView):
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
        return reverse('pending-entry-list')


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


class ApproveEntryView(EntryMixin, StaffuserRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pending-entry-list'

    def get_redirect_url(self, pk):
        entry_qs = Entry.unapproved_objects.all()
        entry = get_object_or_404(entry_qs, pk=pk)
        entry.approved = True
        entry.save()
        return reverse(self.pattern_name)
