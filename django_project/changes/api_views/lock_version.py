# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '8/11/18'

from braces.views import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.views import APIView
from base.models import Project
from ..models import Version


class LockVersion(LoginRequiredMixin, APIView):
    """API to update lock version. Only staff user,
    project owner and managers can view this.

    """

    def get(self, request, project_slug, slug):
        project = Project.objects.get(slug=project_slug)

        # Check permissions
        if not self.request.user.is_staff \
                and self.request.user != project.owner \
                and self.request.user not in project.changelog_managers.all():
            return HttpResponseForbidden(
                "You don't have the necessary permissions to see this.")

        version = Version.objects.get(project=project, slug=slug)
        version.locked = True
        version.save()
        return JsonResponse({'status': 'success'})


class UnlockVersion(LoginRequiredMixin, APIView):
    """API to update lock version.
    Only staff user, project owner and managers can view this.

    """

    def get(self, request, project_slug, slug):
        project = Project.objects.get(slug=project_slug)

        if not self.request.user.is_staff and \
                self.request.user != project.owner \
                and self.request.user not in project.changelog_managers.all():
            return HttpResponseForbidden(
                "You don't have the necessary permissions to see this.")

        version = Version.objects.get(project=project, slug=slug)
        version.locked = False
        version.save()
        return JsonResponse({'status': 'success'})
