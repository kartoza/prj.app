# coding=utf-8
from datetime import datetime
import json
from django.db.models import F
from django.http import HttpResponse
from rest_framework.views import APIView, Response
from rest_framework import status
from base.models.project import Project
from ..models.certifying_organisation import CertifyingOrganisation
from ..models.training_center import TrainingCenter
from ..models.course import Course
from ..serializers.course_serializer import CourseSerializer


class GetUpcomingCourseProject(APIView):
    """API returns GeoJSON location of upcoming courses within a project.
    The location is the location of the training center where this course
    will be held.

    """

    def get(self, request, project_slug):
        try:
            today = datetime.today()
            project = Project.objects.get(slug=project_slug)
            courses = Course.objects.filter(
                certifying_organisation__project=project, start_date__gte=today
            ).order_by(
                'certifying_organisation__name', 'start_date'
            )
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return HttpResponse(
                'Project does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )


class GetUpcomingCourseOrganisation(APIView):
    """API returns GeoJSON location of upcoming courses within a certifying
    organisation. The location is the location of the training center where
    this course will be held.

    """

    def get(self, request, project_slug, organisation_slug):
        today = datetime.today()
        try:
            project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            return HttpResponse(
                'Project does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            organisation = CertifyingOrganisation.objects.get(
                slug=organisation_slug,
                project=project
            )
        except Project.DoesNotExist:
            return HttpResponse(
                'Organisation does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            courses = Course.objects.filter(
                certifying_organisation=organisation, start_date__gte=today
            ).order_by('start_date')
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return HttpResponse(
                'Course does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )


class GetPastCourseProject(APIView):
    """API returns GeoJSON location of upcoming courses within a project.
    The location is the location of the training center where this course
    will be held.

    """

    def get(self, request, project_slug):
        try:
            today = datetime.today()
            project = Project.objects.get(slug=project_slug)
            courses = Course.objects.filter(
                certifying_organisation__project=project, end_date__lte=today
            ).order_by(
                'certifying_organisation__name', 'start_date'
            )
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return HttpResponse(
                'Project does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )


class GetPastCourseOrganisation(APIView):
    """API returns GeoJSON location of upcoming courses within a certifying
    organisation. The location is the location of the training center where
    this course will be held.

    """

    def get(self, request, project_slug, organisation_slug):
        today = datetime.today()
        try:
            project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            return HttpResponse(
                'Project does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            organisation = CertifyingOrganisation.objects.get(
                slug=organisation_slug,
                project=project
            )
        except Project.DoesNotExist:
            return HttpResponse(
                'Organisation does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            courses = Course.objects.filter(
                certifying_organisation=organisation, end_date__lte=today
            ).order_by('start_date')
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return HttpResponse(
                'Course does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )
