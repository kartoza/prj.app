import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    BasePermission, IsAdminUser
)

from base.models import Project
from certification.models.certificate_type import (
    ProjectCertificateType,
    CertificateType
)
from certification.models.checklist import Checklist


class CertificationManagementView(LoginRequiredMixin, ListView):
    context_object_name = 'project_certificate_types'
    template_name = 'certification_management/list.html'
    model = ProjectCertificateType

    def dispatch(self, request, *args, **kwargs):
        """Ensure user has permission to access this view."""
        project = get_object_or_404(Project, slug=self.kwargs['project_slug'])
        manager = project.certification_managers.all()
        if not request.user.is_staff and request.user not in manager:
            raise Http404('Sorry! You have to be staff or certification '
                          'manager to open this page.')
        return super(CertificationManagementView, self).dispatch(
            request, *args, **kwargs
        )

    def get_checklist(self, project: Project):
        """
        Get checklist data for project.
        :return: List of checklist
        """
        checklist = Checklist.objects.filter(
            project=project
        ).order_by('order')
        return checklist

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template."""

        # Navbar data
        self.project_slug = self.kwargs.get('project_slug', None)
        context = super(
            CertificationManagementView, self).get_context_data(*kwargs)
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
            context['checklist'] = self.get_checklist(context['project'])
            context['external_reviewer_text'] = (
                context['the_project'].external_reviewer_invitation
            )

        # certificate types
        context['certificate_types'] = CertificateType.objects.all().order_by(
            'order'
        )
        project = get_object_or_404(Project, slug=self.kwargs['project_slug'])
        context['certificate_types_applied'] = ProjectCertificateType.\
            objects.filter(project=project).values_list(
            'certificate_type', flat=True)

        return context

    def get_queryset(self):
        """Return certificate_types for a project."""

        project = get_object_or_404(Project, slug=self.kwargs['project_slug'])
        return ProjectCertificateType.objects.filter(project=project)


class IsCertificationManager(BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(
            Project,
            slug=request.resolver_match.kwargs.get('project_slug', None))
        return project.certification_managers.filter(
            id=request.user.id).exists()


class ActivateChecklist(APIView):
    permission_classes = [IsAdminUser | IsCertificationManager]

    def post(self, request, project_slug):
        """
        Activate a checklist, only managers and superuser can do this action.
        """
        checklist_id = request.POST.get('checklist_id', None)
        checklist = get_object_or_404(Checklist, id=checklist_id)
        checklist.active = True
        checklist.save()
        return Response({'updated': True})


class ArchiveChecklist(APIView):
    permission_classes = [IsAdminUser | IsCertificationManager]

    def post(self, request, project_slug):
        """
        Archive a checklist, only managers and superuser can do this action.
        """
        checklist_id = request.POST.get('checklist_id', None)
        checklist = get_object_or_404(Checklist, id=checklist_id)
        checklist.active = False
        checklist.save()
        return Response({'updated': True})


class UpdateChecklistOrder(APIView):
    permission_classes = [IsAdminUser | IsCertificationManager]

    def post(self, request, project_slug):
        """
        Update order of checklist

        post data : checklist_order = [
            {
                'id': 1,
                'order': 1
            },...
        ]
        """
        checklist_order = request.POST.get('checklist_order', '[]')
        checklist_order = json.loads(checklist_order)
        for checklist_data in checklist_order:
            try:
                checklist = Checklist.objects.get(id=checklist_data['id'])
                checklist.order = checklist_data['order']
                checklist.save()
            except Checklist.DoesNotExist:
                continue
        return Response({'updated': True})
