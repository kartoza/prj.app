from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from base.models.project import Project
from certification.models.certificate_type import (
    CertificateType, ProjectCertificateType
)
from certification.models.certificate_checklist import CertificateChecklist


class CertificateManagementTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'certificate_management/certificate_management.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template."""

        # Navbar data
        self.project_slug = self.kwargs.get('project_slug', None)
        context = super(
            CertificateManagementTemplateView, self).get_context_data(**kwargs)
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']

        # certificate types
        project = get_object_or_404(Project, slug=self.kwargs['project_slug'])
        context['project_certificate_types'] = ProjectCertificateType.\
            objects.filter(project=project).all()
        context['certificate_types'] = CertificateType.objects.all().order_by(
            'order'
        )
        context['certificate_types_applied'] = ProjectCertificateType.\
            objects.filter(project=project).values_list(
            'certificate_type', flat=True)

        # checklist
        context['certificate_checklists'] = CertificateChecklist.objects.\
            filter(project=project).all().order_by('sort_number')
        return context
