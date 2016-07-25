# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
import logging
import requests
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
    TemplateView,
)
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin
from changes.models import Version
from ..models import Project
from ..forms import ProjectForm
from vota.models import Committee, Ballot
from django.conf import settings

from django.http import HttpResponse, JsonResponse
from allauth.socialaccount.models import SocialToken
from django.core import serializers

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
        context[
            'PROJECT_VERSION_LIST_SIZE'] = settings.PROJECT_VERSION_LIST_SIZE
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
        page_size = settings.PROJECT_VERSION_LIST_SIZE
        context['versions'] = Version.objects.filter(
            project=self.object).order_by('-padded_version')[:page_size]
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
            return qs.filter(owner=self.request.user)


class ProjectCreateView(LoginRequiredMixin, ProjectMixin, CreateView):
    context_object_name = 'project'
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('pending-project-list')

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(ProjectCreateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Project by this name already exists!')


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

    def get_success_url(self):
        if self.object.approved:
            return reverse('project-detail', kwargs={'slug': self.object.slug})
        else:
            return reverse('pending-project-list')

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(ProjectUpdateView, self).form_valid(form)
        except IntegrityError:
            raise ValidationError(
                'ERROR: Version by this name already exists!')


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


class GithubProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'github/populate-github.html'

    def get_context_data(self, **kwargs):
        context = super(
            GithubProjectView, self).get_context_data(**kwargs)
        return context


class JSONResponseMixin(object):
    """A mixin that can be used to render a JSON response."""
    def render_to_json_response(self, context, **response_kwargs):
        """Returns a JSON response, transforming 'context' to make the payload.

        :param context: Context data to use with template
        :type context: dict

        :param response_kwargs: Keyword args
        :type response_kwargs: dict

        :returns A HttpResponse object that contains JSON
        :rtype: HttpResponse
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs)

    @staticmethod
    def convert_context_to_json(context):
        """Convert the context dictionary into a JSON object

        :param context: Context data to use with template
        :type context: dict

        :return: JSON representation of the context
        :rtype: str
        """
        result = '{\n'
        first_flag = True
        for sponsor in context['github_data']:
            if not first_flag:
                result += ',\n'
            result += '    "%s" : "%s"' % (sponsor.id, sponsor.name)
            first_flag = False
        result += '\n}'
        return result


class GithubListView(ProjectMixin, ListView):
    context_object_name = 'project'

    def dispatch(self, request, *args, **kwargs):
        """Ensure this view is only used via ajax.

        :param request: Http request - passed to base class.
        :type request: HttpRequest, WSGIRequest

        :param args: Positional args - passed to base class.
        :type args: tuple

        :param kwargs: Keyword args - passed to base class.
        :type kwargs: dict
        """
        if not request.is_ajax():
            raise Http404("This is an ajax view, friend.")
        return super(GithubListView, self).dispatch(
            request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Render this Project as markdown.

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """
        github_data = self.get_github_data()
        return JsonResponse(github_data, safe=False)

    def get_github_data(self):
        """
        :return:
        """
        retrieved_data = []

        # get user token
        if self.request.user:

            try:
                token = SocialToken.objects.get(
                    account__user=self.request.user.id,
                    account__provider='github'
                )

                if token:
                    response = requests.get(
                        'https://api.github.com/user/repos',
                        params={
                            'access_token': token
                        }
                    )
                    retrieved_data = response.json()
            except SocialToken.DoesNotExist:
                print 'Token not exist'

        return retrieved_data

