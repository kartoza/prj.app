# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
import logging
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
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
from ..models import Project, Domain
from ..forms import ProjectForm, ScreenshotFormset
from vota.models import Committee, Ballot
from changes.models import SponsorshipPeriod
from certification.models import CertifyingOrganisation
from lesson.models.section import Section
from django.conf import settings
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class ProjectMixin(object):
    model = Project
    form_class = ProjectForm


class ProjectBallotListView(ProjectMixin, PaginationMixin, DetailView):
    """List all ballots within in a project."""
    context_object_name = 'project'
    template_name = 'project/ballot-list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        context = super(
            ProjectBallotListView, self).get_context_data(**kwargs)
        committees = Committee.objects.filter(project=self.object)
        ballots = []
        for committee in committees:
            if self.request.user.is_authenticated and \
                    self.request.user in committee.users.all():
                committee_ballots = Ballot.objects.filter(
                        committee=committee)
            else:
                committee_ballots = Ballot.objects.filter(
                    committee=committee).filter(private=False)
            if committee_ballots:
                ballots.append(committee_ballots)
        context['ballots_list'] = ballots
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            projects_qs = Project.approved_objects.all()
        else:
            projects_qs = Project.public_objects.all()
        return projects_qs


class ProjectListView(ProjectMixin, PaginationMixin, ListView):
    """List all approved projects."""
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
        context[
            'PROJECT_VERSION_LIST_SIZE'] = settings.PROJECT_VERSION_LIST_SIZE
        if self.request.user.is_authenticated:
            project = Project.objects.filter(owner=self.request.user)
            pending_organisation = CertifyingOrganisation.objects.filter(
                project__in=project, approved=False
            )
            context['num_project_with_pending'] = 0
            if pending_organisation.exists():
                context['project_with_pending'] = []

                for organisation in pending_organisation:
                    if organisation.project not in \
                            context['project_with_pending']:
                        context['project_with_pending'].append(
                            organisation.project)
                        context['num_project_with_pending'] += 1
                context['message'] = \
                    'You have a pending organisation approval. '
        return context

    def get_queryset(self):
        """Specify the queryset

        Return a specific queryset based on the requesting user's status

        :return: If user.is_authenticated: All approved projects
            If not user.is_authenticated: All public projects
        :rtype: QuerySet

        """
        if self.request.user.is_authenticated:
            projects_qs = Project.approved_objects.all()
        else:
            projects_qs = Project.public_objects.all()

        # filter project query set for custom domain
        try:
            domain = self.request.get_host().split(':')[0]
            custom_domain = Domain.objects.get(domain=domain, approved=True)
            main_organisation = custom_domain.organisation
            projects_qs = projects_qs.filter(organisation=main_organisation)
        except Domain.DoesNotExist:
            projects_qs = projects_qs

        return projects_qs


class ProjectDetailView(ProjectMixin, DetailView):
    context_object_name = 'project'
    template_name = 'project/new_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['projects'] = self.get_queryset()
        context['committees'] = Committee.objects.filter(project=self.object)
        context['versions'] = Version.objects.filter(
            project=self.object).order_by('-padded_version')[:5]
        context['sponsors'] = \
            SponsorshipPeriod.objects.filter(
                project=self.object).order_by('-sponsorship_level__value')
        context['sections'] = \
            Section.objects.filter(
                project=self.object)
        context['screenshots'] = self.object.screenshots.all()
        context['organisations'] = \
            CertifyingOrganisation.objects.filter(
                project=self.object, approved=True)
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
        if not self.request.user.is_authenticated:
            raise Http404

        qs = Project.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(owner=self.request.user)


class ProjectCreateView(LoginRequiredMixin, ProjectMixin, CreateView):
    context_object_name = 'project'
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('home')

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = \
                ScreenshotFormset(self.request.POST, self.request.FILES)
        else:
            context['formset'] = ScreenshotFormset()
        return context

    def form_valid(self, form):
        """Check that form and formset are valid."""
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid() and form.is_valid():
            object = form.save()
            formset.instance = object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


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
            return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = \
                ScreenshotFormset(
                    self.request.POST,
                    self.request.FILES,
                    instance=self.object)
        else:
            context['formset'] = ScreenshotFormset(instance=self.object)
        return context

    def get_success_url(self):
        if self.object.approved:
            return reverse('project-detail', kwargs={'slug': self.object.slug})
        else:
            return reverse('pending-project-list')

    def form_valid(self, form):
        """Check that form and formset are valid."""
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid() and form.is_valid():
            object = form.save()
            formset.instance = object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PendingProjectListView(
        ProjectMixin,
        PaginationMixin,
        ListView,
        StaffuserRequiredMixin,
        LoginRequiredMixin):
    """List all users unapproved projects - staff users see all unapproved."""
    context_object_name = 'projects'
    template_name = 'project/list.html'
    paginate_by = settings.PROJECT_VERSION_LIST_SIZE

    def get_queryset(self):
        projects_qs = Project.unapproved_objects.all()
        if self.request.user.is_staff:
            return projects_qs
        else:
            try:
                return projects_qs.filter(owner=self.request.user)
            except TypeError:
                # LoginRequiredMixin should really be catching this...
                raise Http404('You must be logged in to see pending projects.')

    def get_context_data(self, **kwargs):
        context = super(
            PendingProjectListView, self).get_context_data(**kwargs)
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


def project_sponsor_programme(request, **kwargs):
    """Sponsorship programme view of a project."""

    project_slug = kwargs.get('slug', None)
    project = Project.objects.get(slug=project_slug)

    return render(
        request, 'project/programme.html',
        context={'the_project': project})
