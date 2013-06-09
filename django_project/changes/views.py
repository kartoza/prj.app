import logging
logger = logging.getLogger(__name__)
import datetime
import requests

import logging
logger = logging.getLogger(__name__)

from django.core.urlresolvers import reverse

from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, TemplateView)

from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin


from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView,
    FormView, View
)
from braces.views import LoginRequiredMixin

from .models import Entry


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class EntryMixin(object):
    model = Entry  # implies -> queryset = Entry.objects.all()
    form_class = EntryForm


class EntryCreateUpdateMixin(
        EntryMixin, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(EntryMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class EntryListView(EntryMixin, PaginationMixin, ListView):
    context_object_name = 'sites'
    template_name = 'Entry_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        context['num_sites'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        entries_qs = Entry.objects.for_user(self.request.user)
        return entries_qs


class EntryDetailView(EntryMixin, DetailView):
    context_object_name = 'site'
    template_name = 'Entry_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        entries_qs = (
            Entry.objects.for_user(self.request.user)
            .prefetch_related('site_type')
            .prefetch_related('religions')
        )
        return entries_qs

    def get_object(self, queryset=None):
        obj = super(EntryDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class EntryCreateView(EntryCreateUpdateMixin, CreateView):
    context_object_name = 'site'
    template_name = 'Entry_create.html'

    def get_success_url(self):
        return reverse('entry-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class EntryUpdateView(EntryCreateUpdateMixin, UpdateView):
    context_object_name = 'site'
    template_name = 'Entry_update.html'

    def get_form_kwargs(self):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        return kwargs

    def get_queryset(self):
        entries_qs = Entry.objects
        return entries_qs

    def get_success_url(self):
        return reverse('sacred_site-detail', kwargs={'pk': self.object.pk})
