# coding=utf-8
"""Views for committees."""
# noinspection PyUnresolvedReferences
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import logging
from django.views.generic import DetailView, CreateView
from vota.forms import CreateCommitteeForm
from vota.models import Committee, Ballot

logger = logging.getLogger(__name__)


class CommitteeMixin(object):
    model = Committee
    form_class = CreateCommitteeForm


class CommitteeDetailView(CommitteeMixin, DetailView):
    context_object_name = 'committee'
    template_name = 'committee/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeDetailView, self).get_context_data(**kwargs)
        context['committees'] = self.get_queryset()
        context['openBallots'] = Ballot.open_objects.filter(
            committee=self.get_object())
        context['closedBallots'] = Ballot.closed_objects.filter(
            committee=self.get_object())
        return context

    def get_queryset(self):
        committee_qs = Committee.objects.all()
        return committee_qs

    def get_object(self, queryset=None):
        obj = super(CommitteeDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class CommitteeCreateView(CommitteeMixin, CreateView):
    context_object_name = 'committee'
    template_name = 'committee/create.html'

    def get_success_url(self):
        return reverse('committee-detail', kwargs={
            'project_slug': self.object.project.slug,
            'slug': self.object.slug
        })

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save_m2m()
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
