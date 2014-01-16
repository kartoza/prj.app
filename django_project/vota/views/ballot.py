# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
from django.http import Http404
import logging
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from base.models import Project
from vota.forms import BallotCreateForm
from vota.models import Ballot, Committee

logger = logging.getLogger(__name__)


class BallotMixin(object):
    model = Ballot
    form_class = BallotCreateForm


class BallotDetailView(LoginRequiredMixin, BallotMixin, DetailView):
    context_object_name = 'ballot'
    template_name = 'ballot/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BallotDetailView, self).get_context_data(**kwargs)
        context['committee'] = Committee.objects.get(
            id=self.object.committee.id)
        return context

    def get_queryset(self):
        ballot_qs = Ballot.open_objects.all()
        return ballot_qs

    def get_object(self, queryset=None):
        """
        Get the object for this view.
        Because Ballot slugs are unique within a Committee, we need to make
        sure that we fetch the correct Ballot from the correct Committee
        """
        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            committee_slug = self.kwargs.get('committee_slug', None)
            if slug and project_slug and committee_slug:
                project = Project.objects.get(slug=project_slug)
                committee = Committee.objects.filter(project=project).get(slug=committee_slug)
                obj = queryset.get(slug=slug, committee=committee)
                return obj
            else:
                raise Http404('Sorry! We could not find your ballot!')


class BallotCreateView(LoginRequiredMixin, BallotMixin, CreateView):
    context_object_name = 'ballot'
    template_name = 'ballot/create.html'

    def get_context_data(self, **kwargs):
        context = super(BallotCreateView, self).get_context_data(**kwargs)
        context['committee'] = self.committee
        return context

    def get_form_kwargs(self):
        kwargs = super(BallotCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.committee_slug = self.kwargs.get('committee_slug', None)
        self.committee = Committee.objects.filter(project=self.project)\
            .get(slug=self.committee_slug)
        kwargs.update({
            'user': self.request.user,
            'committee': self.committee
        })
        return kwargs

    def get_success_url(self):
        return reverse('ballot-detail', kwargs={
            'project_slug': self.object.committee.project.slug,
            'committee_slug': self.object.committee.slug,
            'slug': self.object.slug
        })


class BallotUpdateView(LoginRequiredMixin, BallotMixin, UpdateView):
    context_object_name = 'ballot'
    template_name = 'ballot/update.html'

    def get_context_data(self, **kwargs):
        context = super(BallotUpdateView, self).get_context_data(**kwargs)
        context['commitee'] = self.committee
        return context

    def get_form_kwargs(self):
        kwargs = super(BallotUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.committee_slug = self.kwargs.get('committee_slug', None)
        self.committee = Committee.objects.get(slug=self.committee_slug)
        kwargs.update({
            'user': self.request.user,
            'committee': self.committee
        })
        return kwargs

    def get_success_url(self):
        return reverse('ballot-detail', kwargs={
            'project_slug': self.object.committee.project.slug,
            'committee_slug': self.object.committee.slug,
            'slug': self.object.slug
        })


class BallotDeleteView(StaffuserRequiredMixin, BallotMixin, DeleteView):
    context_object_name = 'ballot'
    template_name = 'ballot/delete.html'

    def get_success_url(self):
        return reverse('committee-detail', kwargs={
            'project_slug': self.object.committee.project.slug,
            'slug': self.object.committee.slug
        })

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise Http404
        return Ballot.objects.all()
