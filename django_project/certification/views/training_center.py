# coding=utf-8
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin
from ..models import (
    CertifyingOrganisation,
    TrainingCenter)
from ..forms import TrainingCenterForm


class TrainingCenterMixin(object):
    """Mixin class to provide standard settings for Training Center."""
    model = TrainingCenter
    form_class = TrainingCenterForm


# noinspection PyAttributeOutsideInit
class TrainingCenterCreateView(
        LoginRequiredMixin,
        TrainingCenterMixin, CreateView):
    """Create view for Training Center."""

    context_object_name = 'trainingcenter'
    template_name = 'training_center/create.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the Certifying Organisation detail page
        for the object's parent Certifying Organisation

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.certifying_organisation.project.slug,
            'slug': self.object.certifying_organisation.slug,
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(TrainingCenterCreateView,
                        self).get_context_data(**kwargs)
        context['trainingcenters'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        return context

    def form_valid(self, form):
        """Save new created Training Center

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect

        We check that there is no referential integrity error when saving."""
        try:
            super(TrainingCenterCreateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                'ERROR: Training Center by this name already exists!')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(TrainingCenterCreateView,
                       self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation
        })
        return kwargs
