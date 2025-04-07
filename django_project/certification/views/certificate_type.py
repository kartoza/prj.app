from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from base.models.project import Project
from certification.models.certificate_type import (
    CertificateType, ProjectCertificateType
)

from braces.views import UserPassesTestMixin
from rest_framework import serializers, status
from rest_framework.views import APIView, Response
from django.contrib.sessions.models import Session
from django.utils import timezone


class CerticateTypeSerializer(serializers.ModelSerializer):
    """Serializer for model CertificateType."""

    class Meta:
        model = CertificateType
        fields = '__all__'


class GetCertificateTypeList(UserPassesTestMixin, APIView):
    """API to get list of certificate types."""

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
            project_certificate_types = \
                ProjectCertificateType.objects.filter(
                    project=project
                ).select_related('certificate_type').all()
            certificate_types = [
                pct.certificate_type for pct in project_certificate_types
            ]
            serializer = CerticateTypeSerializer(certificate_types, many=True)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response(
                'Project does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )


def update_project_certificate_view(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    manager = project.certification_managers.all()
    if request.user.is_staff or request.user in manager:
        certificate_types = request.POST.getlist('certificate_types', [])
        for cer in certificate_types:
            certificate_type = get_object_or_404(CertificateType, name=cer)
            obj, created = ProjectCertificateType.objects.get_or_create(
                certificate_type=certificate_type, project=project
            )
        # remove certificate_type that is not in the list
        old_certificate_type = ProjectCertificateType.objects.filter(
            project=project).select_related('certificate_type').all()
        for cer in old_certificate_type:
            if cer.certificate_type.name not in certificate_types:
                ProjectCertificateType.objects.get(
                    certificate_type=cer.certificate_type, project=project
                ).delete()
    return HttpResponseRedirect(
        reverse('certification-management-view',
                kwargs={'project_slug': project_slug})
    )
