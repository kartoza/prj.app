# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
import logging

logger = logging.getLogger(__name__)

from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
)

from braces.views import LoginRequiredMixin
from vota.models import Vote, Ballot
from vota.forms import VoteForm


class VoteCreateUpdateView(LoginRequiredMixin, CreateView):
    context_object_name = 'vote'
    template_name = 'vote/create.html'
    model = Vote
    form_class = VoteForm

    def get_form_kwargs(self):
        kwargs = super(VoteCreateUpdateView, self).get_form_kwargs()
        the_ballot_slug = self.kwargs['ballotSlug']
        the_ballot = Ballot.objects.get(slug=the_ballot_slug)
        try:
            existing_vote = Vote.objects.filter(ballot=the_ballot)\
                .get(user=self.request.user)
            kwargs.update({'instance': existing_vote})
        except Vote.DoesNotExist:
            kwargs.update({'instance': self.object})
        return kwargs

    def form_valid(self, form):
        form.instance.ballot = self.object.ballot
        form.instance.user = self.request.user
        return super(VoteCreateUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ballot-detail',
                       kwargs={'projectSlug':
                               self.object.ballot.committee.project.slug,
                               'committeeSlug':
                               self.object.ballot.committee.slug,
                               'slug': self.object.slug
                               })
