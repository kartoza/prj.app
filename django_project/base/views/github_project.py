# coding=utf-8
"""Views for github project."""
# noinspection PyUnresolvedReferences

import logging
import requests
from django.http import Http404
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView,
    TemplateView,
)
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from ..models import Project
from ..forms import ProjectForm

from django.http import HttpResponse, JsonResponse
from allauth.socialaccount.models import SocialToken

logger = logging.getLogger(__name__)


class ProjectMixin(object):
    model = Project
    form_class = ProjectForm


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
        github_data = self.get_github_repo()
        return JsonResponse(github_data, safe=False)

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
                    retrieved_data = response.json()
            except SocialToken.DoesNotExist:
                print 'Token not exist'

        return retrieved_data
