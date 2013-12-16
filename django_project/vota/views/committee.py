# coding=utf-8
"""Views for projects."""
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
from vota.models import Committee, Ballot


class CommitteeMixin(object):
    model = Committee


class CommitteeCreateUpdateMixin(CommitteeMixin, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(CommitteeMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CommitteeListView(CommitteeMixin, PaginationMixin, ListView):
    """List all approved projects"""
    context_object_name = 'committees'
    template_name = 'committee/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CommitteeListView, self).get_context_data(**kwargs)
        context['num_projects'] = self.get_queryset().count()
        context['unapproved'] = False
        return context

    def get_queryset(self):
        projects_qs = Committee.objects.all()
        return projects_qs


class CommitteeDetailView(CommitteeMixin, DetailView):
    context_object_name = 'committee'
    template_name = 'committee/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeDetailView, self).get_context_data(**kwargs)
        context['ballots'] = Ballot.objects.filter(committee=self.get_object())
        return context

    def get_queryset(self):
        committee_qs = Committee.objects.all()
        return committee_qs

    def get_object(self, queryset=None):
        obj = super(CommitteeDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class CommitteeDeleteView(CommitteeMixin, DeleteView, LoginRequiredMixin):
    context_object_name = 'committee'
    template_name = 'committee/delete.html'

    def get_success_url(self):
        return reverse('project-list')

    def get_queryset(self):
        qs = Committee.all_objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)


class CommitteeCreateView(CommitteeCreateUpdateMixin, CreateView):
    context_object_name = 'committee'
    template_name = 'committee/create.html'

    def get_success_url(self):
        return reverse('pending-project-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdateView(CommitteeCreateUpdateMixin, UpdateView):
    context_object_name = 'committee'
    template_name = 'committee/update.html'

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        return kwargs

    def get_queryset(self):
        qs = Committee.objects
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)

    def get_success_url(self):
        return reverse('committee-list')
