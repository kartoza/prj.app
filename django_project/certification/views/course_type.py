# coding=utf-8
from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    UpdateView)
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin
from ..models import (
    CertifyingOrganisation,
    CourseType)
from ..forms import CourseTypeForm


class CourseTypeMixin(object):
    """Mixin class to provide standard settings for Certifying Organisation."""

    model = CourseType
    form_class = CourseTypeForm


class CourseTypeCreateView(
        LoginRequiredMixin,
        CourseTypeMixin, CreateView):
    """Create view for Course Type."""

    context_object_name = 'coursetype'
    template_name = 'course_type/create.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Certifying Organisation list page
        for the object's parent Project

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

        context = super(CourseTypeCreateView,
                        self).get_context_data(**kwargs)
        context['coursetypes'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseTypeCreateView,
                       self).get_form_kwargs()
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation,
        })
        return kwargs


class CourseTypeUpdateView(LoginRequiredMixin,
                           CourseTypeMixin,
                           UpdateView):
    """Update view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CourseTypeUpdateView,
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

        context = super(CourseTypeUpdateView,
                        self).get_context_data(**kwargs)
        context['coursetypes'] = self.get_queryset() \
            .filter(certifying_organisation=self.certifying_organisation)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: query set that is all Course Type objects
        :rtype: QuerySet
        """

        qs = CourseType.objects.all()
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
            return super(CourseTypeUpdateView,
                         self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Course Type is already exists!')
