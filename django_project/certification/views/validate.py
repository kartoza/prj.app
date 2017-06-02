# coding=utf-8
from django.views.generic import TemplateView


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
        return context
