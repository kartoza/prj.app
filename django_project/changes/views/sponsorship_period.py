__author__ = 'rischan - <--rischan@kartoza.com-->'
__date__ = '12/28/15'

import logging
from base.models import Project

from django.db.models import Q
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
from braces.views import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin

from ..models import SponsorshipPeriod  # noqa
from ..forms import SponsorshipPeriodForm

logger = logging.getLogger(__name__)


class JSONResponseMixin(object):
    """A mixin that can be used to render a JSON response."""
    def render_to_json_response(self, context, **response_kwargs):
        """Returns a JSON response,
        transforming 'context' to make the payload.

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
        for sponsorshipperiod in context['sponsorshipperiods']:
            if not first_flag:
                result += ',\n'
            result += '    "%s" : "%s"' % (
                sponsorshipperiod.id,
                sponsorshipperiod.name)
            first_flag = False
        result += '\n}'
        return result


class SponsorshipPeriodMixin(object):
    """Mixin class to provide standard settings for Sponsorship Period."""
    model = SponsorshipPeriod
    form_class = SponsorshipPeriodForm


class JSONSponsorshipPeriodListView(
        SponsorshipPeriodMixin,
        JSONResponseMixin,
        ListView):
    """List view for Sponsorship Period as json object
     - needed by javascript."""
    context_object_name = 'sponsorshipperiods'

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
        return super(JSONSponsorshipPeriodListView, self).dispatch(
            request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Render this Sponsorship Period as markdown.

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """
        return self.render_to_json_response(context, **response_kwargs)


class SponsorshipPeriodListView(
        SponsorshipPeriodMixin,
        PaginationMixin,
        ListView):
    """List view for Sponsorship Period."""
    context_object_name = 'sponsorshipperiods'
    template_name = 'sponsorship_period/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SponsorshipPeriodListView,
                        self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        project = Project.objects.get(slug=project_slug)
        context['num_sponsorshipperiods'] = \
            self.get_queryset().count()
        context['unapproved'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['project'] = project
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
                queryset = \
                    SponsorshipPeriod.approved_objects.filter(
                        project=project).order_by(
                        '-sponsorship_level__value', '-end_date')

                # Retrofill amount sponsored with sponsorship level value
                # when it is not available
                for index, item in enumerate(queryset):
                    if not queryset[index].amount_sponsored:
                        queryset[index].amount_sponsored = \
                            queryset[index].sponsorship_level.value
                        queryset[index].currency = \
                            queryset[index].sponsorship_level.currency
                        queryset[index].save()
                return queryset
            else:
                raise Http404('Sorry! We could not find your Sponsor Period!')
        return self.queryset


class SponsorshipPeriodDetailView(SponsorshipPeriodMixin, DetailView):
    """Detail view for Sponsorship Period."""
    context_object_name = 'sponsorshipperiod'
    template_name = 'sponsorship_period/detail.html'

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is filtered to only
        show approved Sponsorship Period.
        :rtype: QuerySet
        """
        qs = SponsorshipPeriod.approved_objects.all()
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
                raise Http404('Sorry! We could not find '
                              'your Sponsorship Period!')

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SponsorshipPeriodDetailView,
                        self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        if project_slug:
            context['project'] = Project.objects.get(slug=project_slug)
        return context


# noinspection PyAttributeOutsideInit
class SponsorshipPeriodDeleteView(
        LoginRequiredMixin,
        SponsorshipPeriodMixin,
        DeleteView):
    """Delete view for Sponsorship Period."""
    context_object_name = 'sponsorshipperiod'
    template_name = 'sponsorship_period/delete.html'

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
        self.sponsor_period_slug = self.kwargs.get('slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.sponsorperiod = SponsorshipPeriod.objects.get(
            slug=self.sponsor_period_slug)
        return super(
                SponsorshipPeriodDeleteView,
                self).get(request, *args, **kwargs)

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
        return super(
                SponsorshipPeriodDeleteView,
                self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the Sponsor list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('sponsorshipperiod-list', kwargs={
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
        qs = SponsorshipPeriod.objects.filter(project=self.project)
        return qs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SponsorshipPeriodDeleteView,
                        self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        if project_slug:
            context['project'] = Project.objects.get(slug=project_slug)
        return context


# noinspection PyAttributeOutsideInit
class SponsorshipPeriodCreateView(
        LoginRequiredMixin,
        SponsorshipPeriodMixin,
        CreateView):
    """Create view for Sponsorship Period."""
    context_object_name = 'sponsorshipperiod'
    template_name = 'sponsorship_period/create.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Sponsor list page for the object's parent Project

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('pending-sponsorshipperiod-list', kwargs={
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
                SponsorshipPeriodCreateView,
                self).get_context_data(**kwargs)
        context['sponsorshipperiod'] = self.get_queryset() \
            .filter(project=self.project)
        context['project'] = self.project
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
        kwargs = super(SponsorshipPeriodCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs


# noinspection PyAttributeOutsideInit
class SponsorshipPeriodUpdateView(
        LoginRequiredMixin,
        SponsorshipPeriodMixin,
        UpdateView):
    """Update view for Sponsorship Period."""
    context_object_name = 'sponsorshipperiod'
    template_name = 'sponsorship_period/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(
                SponsorshipPeriodUpdateView,
                self).get_form_kwargs()
        sponsor_period_slug = self.kwargs.get('slug', None)
        self.sponsorperiod = SponsorshipPeriod.objects.get(
            slug=sponsor_period_slug)
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'instance': self.sponsorperiod,
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
                SponsorshipPeriodUpdateView,
                self).get_context_data(**kwargs)
        context['sponsorshipperiod'] = self.get_queryset() \
            .filter(project=self.project)
        context['project'] = self.project
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        projects which user created (staff gets all projects)
        :rtype: QuerySet
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        qs = SponsorshipPeriod.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(
                Q(project=self.project) &
                (Q(author=self.request.user) |
                 Q(project__owner=self.request.user) |
                 Q(project__sponsorship_manager=self.request.user)))

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the Sponsor list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('sponsorshipperiod-list', kwargs={
            'project_slug': self.object.project.slug
        })


class PendingSponsorshipPeriodListView(
        LoginRequiredMixin,
        SponsorshipPeriodMixin,
        PaginationMixin,
        ListView):
    """List view for pending Sponsor."""
    context_object_name = 'sponsorshipperiods'
    template_name = 'sponsorship_period/list.html'
    paginate_by = 10

    def __init__(self):
        """
        We overload __init__ in order to declare self.project and
        self.project_slug. Both are then defined in self.get_queryset
        which is the first method called. This means we can then reuse the
        values in self.get_context_data.
        """
        super(PendingSponsorshipPeriodListView, self).__init__()
        self.project = None
        self.project_slug = None

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(PendingSponsorshipPeriodListView, self)\
            .get_context_data(**kwargs)
        context['num_sponsorshipperiods'] = self.get_queryset().count()
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
                queryset = SponsorshipPeriod.unapproved_objects.filter(
                    project=self.project)
                return queryset
            else:
                raise Http404('Sorry! We could not find '
                              'your Sponsorship Period!')
        return self.queryset


class ApproveSponsorshipPeriodView(
        LoginRequiredMixin,
        SponsorshipPeriodMixin,
        RedirectView):
    """Redirect view for approving Sponsorship Period."""
    permanent = False
    query_string = True
    pattern_name = 'sponsorshipperiod-list'

    def get_redirect_url(self, project_slug, slug):
        """Save Sponsorship Period as approved and redirect

        :param project_slug: The slug of the parent
        Sponsor Period parent Project
        :type project_slug: str

        :param slug: The slug of the Sponsor Level
        :type slug: str

        :returns: URL
        :rtype: str
        """

        if self.request.user.is_staff:
            sponsor_qs = SponsorshipPeriod.unapproved_objects.all()
        else:
            sponsor_qs = SponsorshipPeriod.unapproved_objects.filter(
                Q(project__owner=self.request.user) |
                Q(project__sponsorship_manager=self.request.user)
            )
        sponsor = get_object_or_404(sponsor_qs, slug=slug)
        sponsor.approved = True
        sponsor.save()
        return reverse(self.pattern_name, kwargs={
            'project_slug': project_slug
        })
