import logging
from base.models import Project
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView)
from django.http import HttpResponseRedirect, Http404
from braces.views import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from ..models import TrainingCenter
from ..forms import TrainingCenterForm

logger = logging.getLogger(__name__)


class JSONResponseMixin(object):
    """A mixin that can be used to render a JSON response."""
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.

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
        for trainingcenter in context['trainingcenters']:
            if not first_flag:
                result += ',\n'
            result += '    "%s" : "%s"' % (trainingcenter.id,
                                           trainingcenter.name)
            first_flag = False
        result += '\n}'
        return result


class TrainingCenterMixin(object):
    """Mixin class to provide standard settings for Training Center."""
    model = TrainingCenter
    form_class = TrainingCenterForm


class JSONTrainingCenterListView(TrainingCenterMixin,
                                 JSONResponseMixin, ListView):
    """List view for training center as json object - needed by javascript."""
    context_object_name = 'trainingcenters'

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
        return super(JSONTrainingCenterListView, self).dispatch(
            request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Render this version as markdown.

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """
        return self.render_to_json_response(context, **response_kwargs)


class TrainingCenterListView(
        TrainingCenterMixin,
        PaginationMixin,
        ListView):
    """List view for Training Center."""
    context_object_name = 'trainingcenters'
    template_name = 'training_center/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
                TrainingCenterListView, self).get_context_data(**kwargs)
        context['num_trainingcenters'] = \
            context['trainingcenters'].count()
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Training Center Queryset which is filtered by project
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                project = Project.objects.get(slug=project_slug)
                queryset = TrainingCenter.objects.filter(project=project)
                return queryset
            else:
                raise Http404('Sorry! We could not '
                              'find your training center!')
        return self.queryset


class TrainingCenterDetailView(TrainingCenterMixin, DetailView):
    """Detail view for training center."""
    context_object_name = 'trainingcenter'
    template_name = 'training_center/detail.html'

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is filtered to
        only show approved training center.
        :rtype: QuerySet
        """
        qs = TrainingCenter.approved_objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Training Center slugs are unique within a Project,
        we need to make sure that we fetch the correct
        Training Center from the correct Project

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
                raise Http404('Sorry! We could not '
                              'find your training center!')


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
                TrainingCenterDeleteView,
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
                TrainingCenterDeleteView,
                self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object,
        the User will be redirected
        to the Training Center list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('trainingcenter-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise Http404
        qs = TrainingCenter.objects.filter(project=self.project)
        return qs


# noinspection PyAttributeOutsideInit
class TrainingCenterCreateView(
        LoginRequiredMixin,
        TrainingCenterMixin,
        CreateView):
    """Create view for Training Center."""

    context_object_name = 'trainingcenter'
    template_name = 'training_center/create.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Certifying Organisation list page
        for the object's parent Project

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('trainingcenter-list', kwargs={
            'project_slug': self.object.project.slug,
            'certifyingorganisation_slug':
                self.object.certifying_organisation.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
                TrainingCenterCreateView,
                self).get_context_data(**kwargs)
        context['trainingcenters'] = self.get_queryset() \
            .filter(project=self.project)
        return context

    def form_valid(self, form):
        """Save new created Training Center

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
        kwargs = super(TrainingCenterCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project,
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

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
                TrainingCenterUpdateView,
                self).get_context_data(**kwargs)
        context['trainingcenters'] = self.get_queryset() \
            .filter(project=self.project)
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(TrainingCenterUpdateView, self).get_form_kwargs()
        training_center_slug = self.kwargs.get('slug', None)
        self.trainingcenter = \
            TrainingCenter.objects.get(slug=training_center_slug)
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)

        kwargs.update({
            'user': self.request.user,
            'instance': self.trainingcenter,
            'project': self.project
        })
        return kwargs

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        projects which user created (staff gets all projects)
        :rtype: QuerySet
        """
        qs = TrainingCenter.approved_objects
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the Training Center list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('trainingcenter-list', kwargs={
            'project_slug': self.object.project.slug
        })
