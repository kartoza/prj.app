# coding=utf-8
"""Views for committees."""
# noinspection PyUnresolvedReferences
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.urls import reverse
from django.http import Http404
import logging
from django.views.generic import (
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
    ListView
)
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from base.models import Project
from vota.forms import CreateCommitteeForm
from vota.models import Committee, Ballot

logger = logging.getLogger(__name__)


class CommitteeMixin(object):
    """
    The base mixin for the Committee views
    """
    model = Committee
    form_class = CreateCommitteeForm


class CommitteeDetailView(CommitteeMixin, DetailView):
    """
    The view class for rendering a Committee view
    """
    context_object_name = 'committee'
    template_name = 'committee/detail.html'

    def get_context_data(self, **kwargs):
        """
        We need to add values to the context, primarily for display in the
        navigation.

        :param kwargs: (django dictionary)
        :type kwargs: dict

        :return: context
        :rtype: dict

        """
        context = super(CommitteeDetailView, self).get_context_data(**kwargs)
        context['committees'] = self.get_queryset()
        context['open_ballots'] = Ballot.open_objects.filter(
            committee=self.get_object()).order_by('-closes')
        context['closed_ballots'] = Ballot.closed_objects.filter(
            committee=self.get_object()).order_by('closes')
        return context

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Committee slugs are unique within a Project, we need to make
        sure that we fetch the correct Committee from the correct Project

        :param queryset: A queryset to use to obtain the expected object
        :type queryset: Queryset

        """

        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug', None)
        project_slug = self.kwargs.get('project_slug', None)
        if slug and project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
            except Project.DoesNotExist:
                raise Http404(
                    'The requested project does not exist.'
                )
            try:
                obj = queryset.get(slug=slug, project=project)
                return obj
            except Committee.DoesNotExist:
                raise Http404(
                    'Sorry! The committee you are requesting '
                    'could not be found or you do not have permission to '
                    'view it. Also the committee may not be '
                    'approved yet. Try logging in as a staff member if '
                    'you wish to view it.')
        else:
            raise Http404('Sorry! We could not find your committee!')


# noinspection PyAttributeOutsideInit
class CommitteeListView(CommitteeMixin, ListView):
    """Show all Committees for a Project

    This view returns a list of all Committees within a Project.
    """
    context_object_name = 'committees'
    template_name = 'committee/list.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(CommitteeListView, self).get_context_data(**kwargs)
        context['num_committees'] = self.get_queryset().count()
        context['unapproved'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
        return context

    def get(self, request, *args, **kwargs):
        """Access URL parameters

        We need to define self.project in order to return the correct set of
            Ballot objects

        :param request: Request object
        :type request: HttpRequestObject

        :param args: None

        :param kwargs: (django dict)
        :type kwargs: dict

        """
        project_slug = self.kwargs.get('project_slug')
        try:
            self.project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            raise Http404('Project could not be found')
        return super(CommitteeListView, self).get(
            request, *args, **kwargs
        )

    def get_queryset(self):
        """Specify the queryset

        Return a specific queryset based on the requesting user's status

        :return: All Committees for the current Project
        :rtype: QuerySet

        """
        qs = Committee.objects.filter(project=self.project)
        return qs


# noinspection PyAttributeOutsideInit
class CommitteeCreateView(LoginRequiredMixin, CommitteeMixin, CreateView):

    context_object_name = 'committee'
    template_name = 'committee/create.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeCreateView, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_form_kwargs(self):
        kwargs = super(CommitteeCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def get_success_url(self):
        return reverse('committee-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(CommitteeCreateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Committee by this name already exists!')


# noinspection PyAttributeOutsideInit
class CommitteeUpdateView(LoginRequiredMixin, CommitteeMixin, UpdateView):

    context_object_name = 'committee'
    template_name = 'committee/update.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeUpdateView, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_form_kwargs(self):
        kwargs = super(CommitteeUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise Http404
        return Committee.objects.all()

    def get_success_url(self):
        return reverse('committee-detail', kwargs={
            'project_slug': self.object.project.slug,
            'slug': self.object.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(CommitteeUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Committee by this name already exists!')


# noinspection PyAttributeOutsideInit
class CommitteeDeleteView(StaffuserRequiredMixin, CommitteeMixin, DeleteView):
    """
    The view for deleting a Committee
    """
    context_object_name = 'committee'
    template_name = 'committee/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: Request

        :param args: None
        :type args: dict

        :param kwargs: (django dictionary)
        :type kwargs: dict

        """
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(CommitteeDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: Request

        :param args: None
        :type args: dict

        :param kwargs: (django dictionary)
        :type kwargs: dict

        """
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(CommitteeDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define redirect URL

        The user will be redirected to the detail page for the deleted
        Committee's parent Project

        :return: URL
        :rtype: HttpResponse
        """
        return reverse('project-detail', kwargs={
            'slug': self.project_slug
        })

    def get_queryset(self):
        """Get the queryset for this view

        Because the user must be a staff member, we add an extra validation
        step here.

        :return: Committee queryset if user is staff
        :rtype: Queryset
        :raise Http404: If user is not staff
        """
        if not self.request.user.is_staff:
            raise Http404
        return Committee.objects.filter(project=self.project)
