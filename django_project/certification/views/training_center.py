# coding=utf-8
from base.models import Project
from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView)
from django.http import HttpResponseRedirect, Http404
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


class TrainingCenterDetailView(TrainingCenterMixin, DetailView):
    """Detail view for Training Center."""

    context_object_name = 'trainingcenter'
    template_name = 'training_center/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(TrainingCenterDetailView,
                        self).get_context_data(**kwargs)

        organisation_slug = self.kwargs.get('organisation_slug', None)
        context['organisation_slug'] = organisation_slug
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if organisation_slug:
            context['organisation_slug'] = CertifyingOrganisation.objects.get(
                slug=organisation_slug)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset shows all training center
        :rtype: QuerySet
        """

        qs = TrainingCenter.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because training center slugs are unique within an organisation
        & Project, we need to make sure that we fetch the correct
        training center from the correct certifying organisation

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a project
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            organisation_slug = self.kwargs.get('organisation_slug', None)
            if slug and organisation_slug:
                organisation_slug = CertifyingOrganisation.objects.get(
                    slug=organisation_slug)
                obj = queryset.get(
                    certifying_organisation=organisation_slug, slug=slug)
                return obj
            else:
                raise Http404('Sorry! We could not find '
                              'your Certifying Organisation!')


# noinspection PyAttributeOutsideInit
class TrainingCenterDeleteView(
        LoginRequiredMixin,
        TrainingCenterMixin,
        DeleteView):
    """Delete view for Training Center."""

    context_object_name = 'trainingcenter'
    template_name = 'training_center/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project
        get the organisation_slug from the URL and define
        the certifying organisation.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = CertifyingOrganisation.objects.get(
            slug=self.organisation_slug)
        return super(
            TrainingCenterDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the project_slug & organisation_slug
        from the URL and define the Project & certifying organisation

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        return super(TrainingCenterDeleteView,
                     self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation detail page
        for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the Training Center objects by
        certifying organisation before passing to get_object() to ensure
        that we return the correct training center object.
        The requesting User must be authenticated

        :returns: Training Center queryset filtered by Certifying Organisation
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated():
            raise Http404
        qs = TrainingCenter.objects.filter(
            certifying_organisation=self.certifying_organisation)
        return qs


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
            'project_slug': self.object.project.slug,
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


# noinspection PyAttributeOutsideInit
class TrainingCenterUpdateView(
        LoginRequiredMixin,
        TrainingCenterMixin,
        UpdateView):
    """Update view for Training Center."""

    context_object_name = 'trainingcenter'
    template_name = 'training_center/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(TrainingCenterUpdateView,
                       self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project,
            'certifying_organisation': self.certifying_organisation,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(TrainingCenterUpdateView,
                        self).get_context_data(**kwargs)
        context['trainingcenters'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all
        training center which user created (staff gets all training centers)
        :rtype: QuerySet
        """

        qs = TrainingCenter.objects
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected to
        the Certifying Organisation list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""

        try:
            return super(TrainingCenterUpdateView,
                         self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Training Center by this name already exists!')
