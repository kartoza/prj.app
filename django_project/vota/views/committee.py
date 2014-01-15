# coding=utf-8
"""Views for committees."""
# noinspection PyUnresolvedReferences
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
import logging
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from base.models import Project
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
        """
        Get the object for this view.
        Because Committee slugs are unique within a Project, we need to make
        sure that we fetch the correct Committee from the correct Project
        """
        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            if slug and project_slug:
                project = Project.objects.get(slug=project_slug)
                obj = queryset.get(slug=slug, project=project)
                return obj
            else:
                raise Http404('Sorry! We could not find your committee!')


class CommitteeCreateView(LoginRequiredMixin, CommitteeMixin, CreateView):
    context_object_name = 'committee'
    template_name = 'committee/create.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeCreateView, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_form_kwargs(self):
        kwargs = super(CommitteeCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def get_success_url(self):
        return reverse('committee-detail', kwargs={
            'project_slug': self.object.project.slug,
            'slug': self.object.slug
        })


class CommitteeUpdateView(LoginRequiredMixin, CommitteeMixin, UpdateView):
    context_object_name = 'committee'
    template_name = 'committee/update.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeUpdateView, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_form_kwargs(self):
        kwargs = super(CommitteeUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise Http404
        return Committee.objects.all()

    def get_success_url(self):
        return reverse('committee-detail', kwargs={
            'project_slug': self.object.project.slug,
            'slug': self.object.slug
        })


class CommitteeDeleteView(StaffuserRequiredMixin, CommitteeMixin, DeleteView):
    context_object_name = 'committee'
    template_name = 'committee/delete.html'

    def get_success_url(self):
        return reverse('project-detail', kwargs={
            'slug': self.object.project.slug
        })

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise Http404
        return Committee.objects.all()
