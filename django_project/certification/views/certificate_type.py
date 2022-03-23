from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from base.models.project import Project
from certification.models.certificate_type import (
    CertificateType, ProjectCertificateType
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
