# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,)
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin
from ..models import (
    CertifyingOrganisation,
    Course,)
from ..forms import CourseForm


class CourseMixin(object):
    """Mixin class to provide standard settings for Course."""

    model = Course
    form_class = CourseForm


class CourseCreateView(LoginRequiredMixin, CourseMixin, CreateView):
    """Create view for Course."""

    context_object_name = 'course'
    template_name = 'course/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Certifying Organisation detail page.

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

        context = super(
            CourseCreateView, self).get_context_data(**kwargs)
        context['courses'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseCreateView, self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation,
        })
        return kwargs


class CourseUpdateView(LoginRequiredMixin, CourseMixin, UpdateView):
    """Update view for Course."""

    context_object_name = 'course'
    template_name = 'course/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseUpdateView, self).get_form_kwargs()
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

        context = super(CourseUpdateView, self).get_context_data(**kwargs)
        context['courses'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: All Course objects
        :rtype: QuerySet
        """

        qs = Course.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the Certifying Organisation detail page.

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
            return super(CourseUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Course Convener is already exists!')


class CourseDeleteView(LoginRequiredMixin, CourseMixin, DeleteView):
    """Delete view for Course."""

    context_object_name = 'course'
    template_name = 'course/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the organisation_slug from the URL
        and define the Organisation.

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
        return super(
            CourseDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the organisation_slug from the URL.

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
        return super(
            CourseDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation detail page.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-detail', kwargs={
            'project_slug': self.object.certifying_organisation.project.slug,
            'slug': self.object.certifying_organisation.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Course queryset filtered by Organisation
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated():
            raise Http404
        qs = Course.objects.filter(
            certifying_organisation=self.certifying_organisation)
        return qs
