# coding=utf-8
from django.views.generic import TemplateView
from base.models.project import Project


class ValidateCertificate(TemplateView):
    template_name = 'certificate/validation.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        context = super(
            ValidateCertificate, self).get_context_data(**kwargs)
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
        return context


class ValidateCertificateOrganisation(TemplateView):
    template_name = 'certificate_organisation/validation.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        context = super(
            ValidateCertificateOrganisation, self).get_context_data(**kwargs)
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
        return context
