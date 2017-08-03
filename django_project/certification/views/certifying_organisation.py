# coding=utf-8
from base.models import Project
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView)
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin
from ..models import (
    CertifyingOrganisation,
    TrainingCenter,
    CourseType,
    CourseConvener,
    Course,
    Attendee)
from ..forms import CertifyingOrganisationForm


class JSONResponseMixin(object):
    """A mixin that can be used to render a JSON response."""

    def render_to_json_response(self, context, **response_kwargs):
        """Returns a JSON response, transforming 'context' to make the payload.

        :param context: Context data to use with template
        :type context: dict

        :param response_kwargs: Keyword args
        :type response_kwargs: dict

        :returns A HttpResponse object that contains JSON
        :rtype: HttpResponse
        """

        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs)

    @staticmethod
    def convert_context_to_json(context):
        """Convert the context dictionary into a JSON object.

        :param context: Context data to use with template
        :type context: dict

        :return: JSON representation of the context
        :rtype: str
        """

        result = '{\n'
        first_flag = True
        for certifyingorganisation in context['certifyingorganisations']:
            if not first_flag:
                result += ',\n'
            result += '    "%s" : "%s"' % (certifyingorganisation.id,
                                           certifyingorganisation.name)
            first_flag = False
        result += '\n}'
        return result


class CertifyingOrganisationMixin(object):
    """Mixin class to provide standard settings for Certifying Organisation."""

    model = CertifyingOrganisation
    form_class = CertifyingOrganisationForm


class JSONCertifyingOrganisationListView(
        CertifyingOrganisationMixin, JSONResponseMixin, ListView):
    context_object_name = 'certifyingorganisation'

    def dispatch(self, request, *args, **kwargs):
        """Ensure this view is only used via ajax.

        :param request: Http request - passed to base class.
        :type request: HttpRequest, WSGIRequest

        :param args: Positional args - passed to base class.
        :type args: tuple

        :param kwargs: Keyword args - passed to base class.
        :type kwargs: dict
        """

        if not request.is_ajax():
            raise Http404("This is an ajax view, friend.")
        return super(JSONCertifyingOrganisationListView, self).dispatch(
            request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Render this Certifying Organisation as markdown.

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """

        return self.render_to_json_response(context, **response_kwargs)


class CertifyingOrganisationListView(
        CertifyingOrganisationMixin,
        PaginationMixin,
        ListView):
    """List view for Certifying Organisation."""

    context_object_name = 'certifyingorganisations'
    template_name = 'certifying_organisation/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CertifyingOrganisationListView, self).get_context_data(**kwargs)
        context['num_certifyingorganisations'] = \
            context['certifyingorganisations'].count()
        context['unapproved'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
            context['project'] = context['the_project']
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: CertifyingOrganisation Queryset which is filtered by project.
        :rtype: QuerySet
        :raises: Http404
        """

        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                project = Project.objects.get(slug=project_slug)
                queryset = CertifyingOrganisation.objects.filter(
                    project=project, approved=True, enabled=True)
                return queryset
            else:
                raise Http404('Sorry! We could not find '
                              'your Certifying Organisation!')
        return self.queryset


class CertifyingOrganisationDetailView(
        CertifyingOrganisationMixin,
        DetailView):
    """Detail view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CertifyingOrganisationDetailView, self).get_context_data(**kwargs)

        certifying_organisation = context['certifyingorganisation']
        context['trainingcenters'] = TrainingCenter.objects.filter(
            certifying_organisation=certifying_organisation)
        context['num_trainingcenter'] = context['trainingcenters'].count()
        context['coursetypes'] = CourseType.objects.filter(
            certifying_organisation=certifying_organisation)
        context['num_coursetype'] = context['coursetypes'].count()
        context['courseconveners'] = CourseConvener.objects.filter(
            certifying_organisation=certifying_organisation)
        context['num_courseconvener'] = context['courseconveners'].count()
        context['courses'] = Course.objects.filter(
            certifying_organisation=certifying_organisation)
        context['num_course'] = context['courses'].count()
        project_slug = self.kwargs.get('project_slug', None)
        context['attendee'] = Attendee.objects.filter(
            certifying_organisation=certifying_organisation)
        context['num_attendees'] = context['attendee'].count()
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
            context['project'] = context['the_project']
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is filtered to only show
                    approved Certifying Organisation.
        :rtype: QuerySet
        """

        qs = CertifyingOrganisation.approved_objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Certifying Organisation slugs are unique within a Project,
        we need to make sure that we fetch the correct
        Certifying Organisation from the correct Project

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a project
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            if slug and project_slug:
                project = Project.objects.get(slug=project_slug)
                obj = queryset.get(project=project, slug=slug)
                return obj
            else:
                raise Http404('Sorry! We could not find '
                              'your Certifying Organisation!')


# noinspection PyAttributeOutsideInit
class CertifyingOrganisationDeleteView(
        LoginRequiredMixin,
        CertifyingOrganisationMixin,
        DeleteView):
    """Delete view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project.

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
        return super(
            CertifyingOrganisationDeleteView, self)\
            .get(request, *args, **kwargs)

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

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(
            CertifyingOrganisationDeleteView, self)\
            .post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation list page
        for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the CertifyingOrganisation objects by
        Project before passing to get_object() to ensure that we
        return the correct Certifying Organisation object.
        The requesting User must be authenticated.

        :returns: Certifying Organisation queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated():
            raise Http404
        qs = CertifyingOrganisation.objects.filter(project=self.project)
        return qs


# noinspection PyAttributeOutsideInit
class CertifyingOrganisationCreateView(
        LoginRequiredMixin,
        CertifyingOrganisationMixin,
        CreateView):
    """Create view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the unapproved Certifying Organisation list page
        for the object's parent Project.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('pending-certifyingorganisation-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CertifyingOrganisationCreateView, self).get_context_data(**kwargs)
        context['certifyingorganisations'] = \
            self.get_queryset().filter(project=self.project)
        return context

    def form_valid(self, form):
        """Save new created Certifying Organisation

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect

        We check that there is no referential integrity error when saving."""

        try:
            super(CertifyingOrganisationCreateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                'ERROR: Certifying organisation by this name already exists!')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            CertifyingOrganisationCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs


# noinspection PyAttributeOutsideInit
class CertifyingOrganisationUpdateView(
        LoginRequiredMixin,
        CertifyingOrganisationMixin,
        UpdateView):
    """Update view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            CertifyingOrganisationUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
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
            CertifyingOrganisationUpdateView, self).get_context_data(**kwargs)
        context['certifyingorganisations'] = self.get_queryset() \
            .filter(project=self.project)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        projects which user created (staff gets all projects)
        :rtype: QuerySet
        """

        qs = CertifyingOrganisation.approved_objects
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(organisation_owners=self.request.user)

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the Certifying Organisation list page for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""

        try:
            return super(
                CertifyingOrganisationUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Certifying Organisation by '
                'this name is already exists!')


class PendingCertifyingOrganisationListView(
        StaffuserRequiredMixin,
        CertifyingOrganisationMixin,
        PaginationMixin,
        ListView):
    """List view for pending certifying organisation."""

    context_object_name = 'certifyingorganisations'
    template_name = 'certifying_organisation/pending-list.html'
    paginate_by = 10

    def __init__(self):
        """
        We overload __init__ in order to declare self.project and
        self.project_slug. Both are then defined in self.get_queryset
        which is the first method called. This means we can then reuse the
        values in self.get_context_data.
        """

        super(PendingCertifyingOrganisationListView, self).__init__()
        self.project = None
        self.project_slug = None

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(PendingCertifyingOrganisationListView, self)\
            .get_context_data(**kwargs)
        context['num_certifyingorganisations'] = self.get_queryset().count()
        context['unapproved'] = True
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
        return context

    # noinspection PyAttributeOutsideInit
    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show unapproved
        Certifying Organisation.
        :rtype: QuerySet
        :raises: Http404
        """

        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            if self.project_slug:
                self.project = Project.objects.get(slug=self.project_slug)
                queryset = CertifyingOrganisation.unapproved_objects.filter(
                    project=self.project)
                return queryset
            else:
                raise Http404(
                    'Sorry! We could not find your Certifying Organisation!')
        return self.queryset


class ApproveCertifyingOrganisationView(
        CertifyingOrganisationMixin,
        StaffuserRequiredMixin,
        RedirectView):
    """Redirect view for approving Certifying Organisation."""

    permanent = False
    query_string = True
    pattern_name = 'certifyingorganisation-list'

    def get_redirect_url(self, project_slug, slug):
        """Save Certifying Organisation as approved and redirect.

        :param project_slug: The slug of the parent
                            Certifying Organisation's parent Project.
        :type project_slug: str

        :param slug: The slug of the Certifying Organisation.
        :type slug: str

        :returns: URL
        :rtype: str
        """

        certifyingorganisation_qs = \
            CertifyingOrganisation.unapproved_objects.all()
        certifyingorganisation = \
            get_object_or_404(certifyingorganisation_qs, slug=slug)
        certifyingorganisation.approved = True
        certifyingorganisation.save()
        return reverse(self.pattern_name, kwargs={
            'project_slug': project_slug
        })
