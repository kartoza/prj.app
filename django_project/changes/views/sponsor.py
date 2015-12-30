__author__ = 'rischan'


import logging
from base.models import Project

logger = logging.getLogger(__name__)

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

from ..models import Sponsor, SponsorshipPeriod, Version  # noqa
from ..forms import SponsorForm, SponsorRenewedForm


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
        """Convert the context dictionary into a JSON object

        :param context: Context data to use with template
        :type context: dict

        :return: JSON representation of the context
        :rtype: str
        """
        result = '{\n'
        first_flag = True
        for sponsor in context['sponsors']:
            if not first_flag:
                result += ',\n'
            result += '    "%s" : "%s"' % (sponsor.id, sponsor.name)
            first_flag = False
        result += '\n}'
        return result


class SponsorMixin(object):
    """Mixin class to provide standard settings for Sponsor."""
    model = Sponsor  # implies -> queryset = Sponsor.objects.all()
    form_class = SponsorForm


class SponsorRenewedMixin(object):
    """Mixin class to provide standard settings for Renewed sponsor."""
    model = SponsorshipPeriod
    form_class = SponsorRenewedForm


class JSONSponsorListView(SponsorMixin, JSONResponseMixin, ListView):
    """List view for Sponsor as json object - needed by javascript."""
    context_object_name = 'sponsors'

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
        return super(JSONSponsorListView, self).dispatch(
            request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Render this Sponsor as markdown.

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """
        return self.render_to_json_response(context, **response_kwargs)

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Sponsors
        of project.
        :rtype: QuerySet
        :raises: Http404
        """
        sponsor_id = self.kwargs['sponsor']
        sponsor = get_object_or_404(Sponsor, id=sponsor_id)
        qs = Sponsor.approved_objects.filter(project=sponsor.project)
        return qs


class SponsorListView(SponsorMixin, PaginationMixin, ListView):
    """List view for Sponsor."""
    context_object_name = 'sponsors'
    template_name = 'sponsor/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SponsorListView, self).get_context_data(**kwargs)
        context['num_sponsors'] = context['sponsors'].count()
        context['unapproved'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Sponsor Queryset which is filtered by project
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                project = Project.objects.get(slug=project_slug)
                queryset = Sponsor.objects.filter(project=project)
                return queryset
            else:
                raise Http404('Sorry! We could not find your Sponsor!')
        return self.queryset


class SponsorDetailView(SponsorMixin, DetailView):
    """Detail view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/detail.html'

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is filtered to only show approved Sponsor.
        :rtype: QuerySet
        """
        qs = Sponsor.approved_objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Sponsor slugs are unique within a Project, we need to make
        sure that we fetch the correct Sponsor from the correct Project

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
                raise Http404('Sorry! We could not find your sponsor!')


# noinspection PyAttributeOutsideInit
class SponsorDeleteView(LoginRequiredMixin, SponsorMixin, DeleteView):
    """Delete view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project

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
        return super(SponsorDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project

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
        return super(SponsorDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the Sponsor list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('sponsor-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the Sponsor objects by Project before passing to
        get_object() to ensure that we return the correct Sponsor object.
        The requesting User must be authenticated

        :returns: Sponsor queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """
        if not self.request.user.is_authenticated():
            raise Http404
        qs = Sponsor.objects.filter(project=self.project)
        return qs


# noinspection PyAttributeOutsideInit
class SponsorCreateView(LoginRequiredMixin, SponsorMixin, CreateView):
    """Create view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/create.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Sponsor list page for the object's parent Project

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('pending-sponsor-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SponsorCreateView, self).get_context_data(**kwargs)
        context['sponsors'] = self.get_queryset() \
            .filter(project=self.project)
        return context

    def form_valid(self, form):
        """Save new created Sponsor

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect
        """
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SponsorCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(SponsorCreateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Sponsor by this name already exists!')


# noinspection PyAttributeOutsideInit
class SponsorRenewedView(LoginRequiredMixin, SponsorRenewedMixin, CreateView):
    """Renewed view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/renewed.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Sponsor list page for the object's parent Project

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('pending-sponsor-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Save renewed sponsor

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect
        """
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SponsorRenewedView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs


# noinspection PyAttributeOutsideInit
class SponsorUpdateView(LoginRequiredMixin, SponsorMixin, UpdateView):
    """Update view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SponsorUpdateView, self).get_form_kwargs()
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
        context = super(SponsorUpdateView, self).get_context_data(**kwargs)
        context['sponsors'] = self.get_queryset() \
            .filter(project=self.project)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        projects which user created (staff gets all projects)
        :rtype: QuerySet
        """
        qs = Sponsor.approved_objects
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the Sponsor list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('sponsor-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(SponsorUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Sponsor by this name already exists!')


class PendingSponsorListView(StaffuserRequiredMixin, SponsorMixin,
                             PaginationMixin, ListView):  # noqa
    """List view for pending Sponsor."""
    context_object_name = 'sponsors'
    template_name = 'sponsor/list.html'
    paginate_by = 10

    def __init__(self):
        """
        We overload __init__ in order to declare self.project and
        self.project_slug. Both are then defined in self.get_queryset
        which is the first method called. This means we can then reuse the
        values in self.get_context_data.
        """
        super(PendingSponsorListView, self).__init__()
        self.project = None
        self.project_slug = None

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(PendingSponsorListView, self)\
            .get_context_data(**kwargs)
        context['num_sponsors'] = self.get_queryset().count()
        context['unapproved'] = True
        context['project_slug'] = self.project_slug
        context['project'] = self.project
        return context

    # noinspection PyAttributeOutsideInit
    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show unapproved
        Sponsor.
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            if self.project_slug:
                self.project = Project.objects.get(slug=self.project_slug)
                queryset = Sponsor.unapproved_objects.filter(
                    project=self.project)
                return queryset
            else:
                raise Http404('Sorry! We could not find your sponsor!')
        return self.queryset


class ApproveSponsorView(SponsorMixin, StaffuserRequiredMixin, RedirectView):
    """Redirect view for approving Sponsor."""
    permanent = False
    query_string = True
    pattern_name = 'sponsor-list'

    def get_redirect_url(self, project_slug, slug):
        """Save Sponsor as approved and redirect

        :param project_slug: The slug of the parent Sponsor's parent Project
        :type project_slug: str

        :param slug: The slug of the Sponsor
        :type slug: str

        :returns: URL
        :rtype: str
        """
        sponsor_qs = Sponsor.unapproved_objects.all()
        sponsor = get_object_or_404(sponsor_qs, slug=slug)
        sponsor.approved = True
        sponsor.save()
        return reverse(self.pattern_name, kwargs={
            'project_slug': project_slug
        })
