# coding=utf-8
"""Helpers for submitting issues to github."""
import json
import requests
from django.views.generic import View
from django.conf import settings
from braces.views import LoginRequiredMixin
from django.http import HttpResponse


class GithubIssue(LoginRequiredMixin, View):
    """
    Send an issue to github.

    View is called via ajax. Calling function expects either status code 200
    if everything is ok, or any error status code to alert the user.
    GIT_USER and GIT_PASSWORD are expected from os.environ
    """
    # noinspection PyUnusedLocal
    def post(self, request, *args, **kwargs):
        """Post the form with issue content to github.

        :param request: request supplied by inherited view. At minimum the
            request dictionary should include **title** and **desc**
            key/values.
        :param args: positional arguments supplied by view.
        :param kwargs: keyword arguments supplied by view.

        :returns: HttpResponse - 200 if all well, otherwise 500
        :rtype: HttpResponse

        """
        # noinspection PyUnresolvedReferences
        title = request.POST['title'] + ' by ' + self.request.user.username
        data = json.dumps({'title': title, 'body': request.POST['desc']})
        if settings.GITHIB_USER and settings.GITHUB_PASSWORD:
            r = requests.post(
                settings.GITHUB_URL, data,
                auth=(settings.GITHUB_USER, settings.GITHUB_PASSWORD))
            if r.status_code == 201:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=500)
        else:
            return HttpResponse(status=500)
