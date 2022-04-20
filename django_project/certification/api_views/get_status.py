# coding=utf-8
from braces.views import UserPassesTestMixin
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.views import APIView, Response
from base.models.project import Project
from ..models.status import Status


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for model Status."""

    class Meta:
        model = Status
        fields = '__all__'


class GetStatus(UserPassesTestMixin, APIView):

    """API to get list of status."""

    def test_func(self, user):
        if not user.is_anonymous:
            return True
        else:
            session = self.request.GET.get('s', None)
            try:
                session = Session.objects.get(
                    pk=session
                )
                return (
                    session.expire_date > timezone.now()
                )
            except Session.DoesNotExist:
                return False

    def get(self, request, project_slug):
        try:
            project = Project.objects.get(slug=project_slug)
            status_qs = Status.objects.filter(project=project)
            serializer = StatusSerializer(status_qs, many=True)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return HttpResponse(
                'Project does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )
