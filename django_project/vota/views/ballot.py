# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
import logging
from django.views.generic import DetailView
from vota.models import Ballot, Committee

logger = logging.getLogger(__name__)


class BallotMixin(object):
    model = Ballot


class BallotDetailView(BallotMixin, DetailView):
    context_object_name = 'ballot'
    template_name = 'ballot/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BallotDetailView, self).get_context_data(**kwargs)
        context['allBallots'] = Ballot.objects.all()
        context['committee'] = Committee.objects.get(
            id=self.object.committee.id)
        context['userVoted'] = Ballot.get_user_voted(self.object,
                                                     user=self.request.user)
        return context

    def get_queryset(self):
        ballot_qs = Ballot.open_objects.all()
        return ballot_qs
