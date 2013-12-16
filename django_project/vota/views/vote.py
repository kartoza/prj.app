# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
import logging

logger = logging.getLogger(__name__)

from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
)

from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin
from vota.models import Vote, Ballot
from vota.forms import VoteForm


class VoteMixin(object):
    model = Vote
    form_class = VoteForm


class VoteCreateUpdateMixin(VoteMixin, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(VoteMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class VoteCreateView(VoteCreateUpdateMixin, CreateView):
    context_object_name = 'vote'
    template_name = 'vote/create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        data = super(VoteCreateView, self).get_context_data(**kwargs)
        ballot_id = self.kwargs['ballotID']
        ballot_obj = Ballot.objects.get(id=ballot_id)
        data.get('form').initial['user'] = self.request.user
        data.get('form').initial['ballot'] = ballot_obj
        return data
