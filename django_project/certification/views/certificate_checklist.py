import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse

from base.models.project import Project
from certification.models.certificate_checklist import (
    CertificateChecklist
)


class CertificateChecklistMixin():
    """Mixin class to provide standard settings for Certificate Checklist."""
    model = CertificateChecklist


class CertificateChecklistCreateView(LoginRequiredMixin,
                                     CertificateChecklistMixin,
                                     CreateView):
    """Create view for certificate checklist question."""

    context_object_name = 'question'
    template_name = 'certificate_checklist/create.html'
    fields = ['question', 'is_additional_response_enabled']

    def get_success_url(self):
        project_slug = self.kwargs.get('project_slug', None)
        return reverse('certificate-management', kwargs={
            'project_slug': project_slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template."""

        # Navbar data
        self.project_slug = self.kwargs.get('project_slug', None)
        context = super().get_context_data(**kwargs)
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
        return context

    def form_valid(self, form):
        project_slug = self.kwargs.get('project_slug', None)
        project = get_object_or_404(Project, slug=project_slug)
        form.instance.project = project
        return super(CertificateChecklistCreateView, self).form_valid(form)


class CertificateChecklistUpdateView(LoginRequiredMixin,
                                     CertificateChecklistMixin,
                                     UpdateView):
    """Update order view for Certificate Checklist."""

    def post(self, request, *args, **kwargs):
        checklist_json = request.body

        try:
            checklist_request = json.loads(checklist_json)
        except ValueError:
            raise Http404(
                'Error json values'
            )

        for cl in checklist_request:
            checklist = CertificateChecklist.objects.get(id=cl['id'])
            sort_number = cl.get('sort_number', None)
            is_archived = cl.get('is_archived', None)
            if checklist:
                if sort_number is not None:
                    checklist.sort_number = sort_number
                if is_archived is not None:
                    checklist.is_archived = is_archived
                checklist.save()

        return HttpResponse('')
