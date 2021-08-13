# coding=utf-8
from django.urls import reverse
from django.http import Http404
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
    DetailView)
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin
from base.models import Project
from ..models import (
    CertifyingOrganisation,
    CourseType)
from ..forms import CourseTypeForm


class CourseTypeMixin(object):
    """Mixin class to provide standard settings for Course Type."""

    model = CourseType
    form_class = CourseTypeForm


class CourseTypeCreateView(
        LoginRequiredMixin,
        CourseTypeMixin, CreateView):
    """Create view for Course Type."""

    context_object_name = 'coursetype'
    template_name = 'course_type/create.html'

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
            CourseTypeCreateView, self).get_context_data(**kwargs)
        context['coursetypes'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        context['organisation'] = CertifyingOrganisation.objects.get(
            slug=self.kwargs.get('organisation_slug', None)
        )
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseTypeCreateView, self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation,
        })
        return kwargs


class CourseTypeDeleteView(
        LoginRequiredMixin,
        CourseTypeMixin,
        DeleteView):
    """Delete view for Course Type."""

    context_object_name = 'coursetype'
    template_name = 'course_type/delete.html'

    def get(self, request, *args, **kwargs):
        """
        Get the organisation_slug from the URL and define the Organisation.

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
            CourseTypeDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project.

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
        return super(CourseTypeDeleteView, self).post(request, *args, **kwargs)

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

        :returns: Course Type queryset filtered by Certifying Organisation
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated:
            raise Http404
        qs = CourseType.objects.filter(
            certifying_organisation=self.certifying_organisation)
        return qs


class CourseTypeUpdateView(
        LoginRequiredMixin,
        CourseTypeMixin,
        UpdateView):
    """Update view for Course Type."""

    context_object_name = 'coursetype'
    template_name = 'course_type/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            CourseTypeUpdateView, self).get_form_kwargs()
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

        context = super(
            CourseTypeUpdateView, self).get_context_data(**kwargs)
        context['coursetypes'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        context['organisation'] = CertifyingOrganisation.objects.get(
            slug=self.kwargs.get('organisation_slug', None)
        )
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: query set that is all Course Type objects
        :rtype: QuerySet
        """

        qs = CourseType.objects.all()
        return qs

    def get_success_url(self):
        """Define the redirect URL.

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
            return super(
                CourseTypeUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Course Type already exists!')


class CourseTypeDetailView(
        CourseTypeMixin, DetailView):
    """Detail view for Course Type."""

    context_object_name = 'coursetype'
    template_name = 'course_type/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        context = super(
            CourseTypeDetailView, self).get_context_data(**kwargs)
        context['coursetypes'] = CourseType.objects.filter(
            certifying_organisation=self.certifying_organisation)
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
            context['project'] = context['the_project']
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all course type in the
            corresponding organisation.
        :rtype: QuerySet
        """

        qs = CourseType.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a course type
            within the organisation.
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            queryset = self.get_queryset()
            pk = self.kwargs.get('pk', None)
            organisation_slug = self.kwargs.get('organisation_slug', None)
            if pk and organisation_slug:
                certifying_organisation = \
                    CertifyingOrganisation.objects.get(slug=organisation_slug)
                obj = queryset.get(
                    certifying_organisation=certifying_organisation, pk=pk)
                return obj
            else:
                raise Http404('Sorry! We could not find your course type!')
