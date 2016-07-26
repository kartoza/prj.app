# coding=utf-8
"""Views for github project."""
# noinspection PyUnresolvedReferences

import json
import logging
import requests
from django.http import Http404
from django.views.generic import (
    ListView,
    UpdateView,
    RedirectView,
    TemplateView,
)
from braces.views import LoginRequiredMixin
from ..models import Project
from ..forms import ProjectForm

from django.http import HttpResponse, JsonResponse
from allauth.socialaccount.models import SocialToken

logger = logging.getLogger(__name__)


class ProjectMixin(object):
    model = Project
    form_class = ProjectForm


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


class GithubProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'github/populate-github.html'

    def get_context_data(self, **kwargs):
        context = super(
            GithubProjectView, self).get_context_data(**kwargs)

        context['has_github_account'] = SocialToken.objects.filter(
                account__user=self.request.user.id,
                account__provider='github'
            ).exists()

        return context


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
        github_data = self.get_github_repo()
        return JsonResponse(github_data, safe=False)

    def check_project_existence(self, github_projects):
        """
        Check whether project already in db
        :param github_projects: list github projects
        :return: modified list github projects with additional parameter
        """
        for g_project in github_projects:
            if Project.objects.filter(slug=g_project['name']).exists():
                g_project['added'] = True
            else:
                g_project['added'] = False
        return github_projects

    def get_github_repo(self):
        """Get github repos from github api
        :return: github repo dictionary
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
                    retrieved_data = self.check_project_existence(
                        response.json()
                    )
            except SocialToken.DoesNotExist:
                print 'Token not exist'

        return retrieved_data


class GithubSubmitView(LoginRequiredMixin, ProjectMixin, UpdateView):
    """Add github project"""
    context_object_name = 'project'

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        :raises: Http404
        """
        github_data_json = request.body
        retrieved_data = {}

        try:
            github_data = json.loads(github_data_json)
        except ValueError:
            raise Http404(
                'Error json values'
            )

        if self.request.user:
            try:
                token = SocialToken.objects.get(
                    account__user=self.request.user.id,
                    account__provider='github'
                )

                if token:
                    response = requests.get(
                        'https://api.github.com/repos/'+github_data['full_name'],
                        params={
                            'access_token': token
                        }
                    )
                    retrieved_data = response.json()

                if retrieved_data:
                    new_project = Project(
                        name=retrieved_data['name'],
                    )

                    new_project.description = retrieved_data['description']
                    new_project.owner = self.request.user
                    new_project.slug = retrieved_data['name']
                    new_project.private = retrieved_data['private']
                    new_project.gitter_room = retrieved_data['full_name']

                    new_project.save()

            except SocialToken.DoesNotExist:
                print 'Token not exist'

        return HttpResponse('')
