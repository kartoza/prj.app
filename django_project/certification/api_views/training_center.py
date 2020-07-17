# coding=utf-8
import json
from django.http import HttpResponse
from rest_framework.views import APIView, Response
from rest_framework import status
from base.models.project import Project
from ..models.certifying_organisation import CertifyingOrganisation
from ..models.training_center import TrainingCenter
from ..utilities import CustomSerializer


class GetTrainingCenterProjectLocation(APIView):
    """API returns GeoJSON location of training center within a project."""

    def get(self, request, project_slug):
        try:
            project = Project.objects.get(slug=project_slug)
            training_centers = TrainingCenter.objects.filter(
                certifying_organisation__project=project
            ).order_by('certifying_organisation__name')
            serializers = CustomSerializer()
            data = (
                serializers.serialize(
                    training_centers,
                    geometry_field='location',
                    fields=('name', 'certifying_organisation__name')
                )
            )
            return Response(json.loads(data))
        except Project.DoesNotExist:
            return HttpResponse(
                'Project does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )


class GetTrainingCenterOrganisationLocation(APIView):
    """API returns GeoJSON location of training center within
    a certifying organisation.

    """

    def get(self, request, project_slug, organisation_slug):
        try:
            project = Project.objects.get(slug=project_slug)
            organisation = CertifyingOrganisation.objects.get(
                slug=organisation_slug,
                project=project
            )
            training_centers = TrainingCenter.objects.filter(
                certifying_organisation=organisation
            ).order_by('name')
            serializers = CustomSerializer()
            data = (
                serializers.serialize(
                    training_centers,
                    geometry_field='location',
                    fields=('name', 'certifying_organisation__name')
                )
            )
            return Response(json.loads(data))
        except Project.DoesNotExist:
            return HttpResponse(
                'Project does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )
