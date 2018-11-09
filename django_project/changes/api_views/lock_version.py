# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '8/11/18'

from braces.views import StaffuserRequiredMixin
from django.http import JsonResponse
from rest_framework.views import APIView
from base.models import Project
from ..models import Version


class LockVersion(StaffuserRequiredMixin, APIView):
    """API to update lock version. Only staff user can view this."""

    def get(self, request, project_slug, slug):
        project = Project.objects.get(slug=project_slug)
        version = Version.objects.get(project=project, slug=slug)
        version.locked = True
        version.save()
        return JsonResponse({'status': 'success'})


class UnlockVersion(StaffuserRequiredMixin, APIView):
    """API to update lock version. Only staff user can view this."""

    def get(self, request, project_slug, slug):
        project = Project.objects.get(slug=project_slug)
        version = Version.objects.get(project=project, slug=slug)
        version.locked = False
        version.save()
        return JsonResponse({'status': 'success'})
