from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from base.models.project import Project
from certification.models.certificate_type import (
    CertificateType, ProjectCertificateType
)


class ProjectCertificateTypeView(LoginRequiredMixin, ListView):
    context_object_name = 'project_certificate_types'
    template_name = 'certificate_type/list.html'
    model = ProjectCertificateType

    def dispatch(self, request, *args, **kwargs):
        """Ensure user has permission to access this view."""
        project = get_object_or_404(Project, slug=self.kwargs['project_slug'])
        manager = project.certification_managers.all()
        if not request.user.is_staff and request.user not in manager:
            raise Http404('Sorry! You have to be staff or certification '
                          'manager to open this page.')
        return super(ProjectCertificateTypeView, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template."""

        # Navbar data
        self.project_slug = self.kwargs.get('project_slug', None)
        context = super(
            ProjectCertificateTypeView, self).get_context_data(*kwargs)
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']

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


def updateProjectCertificateView(request, project_slug):
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
        reverse('certificate-type-list', kwargs={'project_slug': project_slug})
    )
