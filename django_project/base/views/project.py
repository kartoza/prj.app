# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
import logging
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView,
)
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin
from changes.models import Version
from ..models import Project
from ..forms import ProjectForm
from vota.models import Committee, Ballot

logger = logging.getLogger(__name__)


class ProjectMixin(object):
    model = Project
    form_class = ProjectForm


class ProjectBallotListView(ProjectMixin, PaginationMixin, DetailView):
    """List all ballots within in a project"""
    context_object_name = 'project'
    template_name = 'project/ballot-list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        context = super(ProjectBallotListView, self).get_context_data(**kwargs)
        committees = Committee.objects.filter(project=self.object)
        ballots = []
        for committee in committees:
            if self.request.user.is_authenticated and \
                    self.request.user in committee.users.all():
                    committee_ballots = Ballot.objects.filter(
                        committee=committee)
            else:
                committee_ballots = Ballot.objects.filter(committee=committee)\
                    .filter(private=False)
            if committee_ballots:
                ballots.append(committee_ballots)
        context['ballots_list'] = ballots
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated():
            projects_qs = Project.approved_objects.all()
        else:
            projects_qs = Project.public_objects.all()
        return projects_qs


class ProjectListView(ProjectMixin, PaginationMixin, ListView):
    """List all approved projects"""
    context_object_name = 'projects'
    template_name = 'project/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Add to the view's context data

        :param kwargs: (django dictionary)
        :type kwargs: dict

        :return: context
        :rtype: dict

        """
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['num_projects'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        """Specify the queryset

        Return a specific queryset based on the requesting user's status

        :return: If user.is_authenticated: All approved projects
            If not user.is_authenticated: All public projects
        :rtype: QuerySet

        """
        if self.request.user.is_authenticated():
            projects_qs = Project.approved_objects.all()
        else:
            projects_qs = Project.public_objects.all()
        return projects_qs


class ProjectDetailView(ProjectMixin, DetailView):
    context_object_name = 'project'
    template_name = 'project/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['projects'] = self.get_queryset()
        context['committees'] = Committee.objects.filter(project=self.object)
        context['versions'] = Version.objects.filter(
            project=self.object).order_by('-padded_version')
        return context

    def get_queryset(self):
        projects_qs = Project.approved_objects.all()
        return projects_qs

    def get_object(self, queryset=None):
        obj = super(ProjectDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class ProjectDeleteView(LoginRequiredMixin, ProjectMixin, DeleteView):
    context_object_name = 'project'
    template_name = 'project/delete.html'

    def get_success_url(self):
        return reverse('project-list')

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise Http404

        qs = Project.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)


class ProjectCreateView(LoginRequiredMixin, ProjectMixin, CreateView):
    context_object_name = 'project'
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('pending-project-list')

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ProjectUpdateView(LoginRequiredMixin, ProjectMixin, UpdateView):
    context_object_name = 'project'
    template_name = 'project/update.html'

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_queryset(self):
        qs = Project.objects
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)

    def get_success_url(self):
        return reverse('project-detail', kwargs={'slug': self.object.slug})


class PendingProjectListView(
        ProjectMixin, PaginationMixin, ListView, StaffuserRequiredMixin):
    """List all users unapproved projects - staff users see all unapproved."""
    context_object_name = 'projects'
    template_name = 'project/list.html'
    paginate_by = 1000

    def get_queryset(self):
        projects_qs = Project.unapproved_objects.all()
        if self.request.user.is_staff:
            return projects_qs
        else:
            return projects_qs.filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(PendingProjectListView,
                        self).get_context_data(**kwargs)
        context['num_projects'] = self.get_queryset().count()
        context['unapproved'] = True
        return context


class ApproveProjectView(StaffuserRequiredMixin, ProjectMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pending-project-list'

    def get_redirect_url(self, slug):
        projects_qs = Project.unapproved_objects.all()
        project = get_object_or_404(projects_qs, slug=slug)
        project.approved = True
        project.save()
        return reverse(self.pattern_name)
