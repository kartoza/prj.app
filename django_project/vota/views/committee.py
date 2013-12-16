# coding=utf-8
"""Views for committees."""
# noinspection PyUnresolvedReferences
import logging
from django.views.generic import DetailView
from vota.models import Committee, Ballot

logger = logging.getLogger(__name__)


class CommitteeMixin(object):
    model = Committee


class CommitteeDetailView(CommitteeMixin, DetailView):
    context_object_name = 'committee'
    template_name = 'committee/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeDetailView, self).get_context_data(**kwargs)
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
