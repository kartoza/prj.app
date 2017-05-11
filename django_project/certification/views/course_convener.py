# coding=utf-8
from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView)
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin
from ..models import CertifyingOrganisation, CourseConvener
from ..forms import CourseConvenerForm


class CourseConvenerMixin(object):
    """Mixin class to provide standard settings for Course Convener."""

    model = CourseConvener
    form_class = CourseConvenerForm


class CourseConvenerCreateView(
        LoginRequiredMixin,
        CourseConvenerMixin, CreateView):
    """Create view for Course Convener."""

    context_object_name = 'convener'
    template_name = 'course_convener/create.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the Certifying Organisation detail page

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.certifying_organisation.project.slug,
            'slug': self.object.certifying_organisation.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(CourseConvenerCreateView,
                        self).get_context_data(**kwargs)
        context['conveners'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        return context

    def form_valid(self, form):
        """Save new created Course Convener

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect

        We check that there is no referential integrity error when saving."""

        try:
            super(CourseConvenerCreateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                'ERROR: Certifying organisation by this name already exists!')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseConvenerCreateView,
                       self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation
        })
        return kwargs


class CourseConvenerDeleteView(
        LoginRequiredMixin,
        CourseConvenerMixin,
        DeleteView):
    """Delete view for Course Convener."""

    context_object_name = 'convener'
    template_name = 'course_convener/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the organisation_slug from the URL
        and define the Organisation

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        return super(CourseConvenerDeleteView,
                     self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the organisation_slug from the URL

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        return super(CourseConvenerDeleteView,
                     self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation detail page

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.certifying_organisation.project.slug,
            'slug': self.object.certifying_organisation.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Course Convener queryset filtered by Organisation
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated():
            raise Http404
        qs = CourseConvener.objects.filter(
            certifying_organisation=self.certifying_organisation)
        return qs


class CourseConvenerUpdateView(LoginRequiredMixin,
                               CourseConvenerMixin,
                               UpdateView):
    """Update view for Course Convener."""

    context_object_name = 'convener'
    template_name = 'course_convener/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseConvenerUpdateView,
                       self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(CourseConvenerUpdateView,
                        self).get_context_data(**kwargs)
        context['conveners'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: All Course Convener objects
        :rtype: QuerySet
        """

        qs = CourseConvener.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected to
        the Certifying Organisation detail page

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.certifying_organisation.project.slug,
            'slug': self.object.certifying_organisation.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""

        try:
            return super(CourseConvenerUpdateView,
                         self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Course Convener is already exists!')
