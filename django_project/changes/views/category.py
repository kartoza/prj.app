# -*- coding: utf-8 -*-
"""**View classes for Category**

"""
# noinspection PyUnresolvedReferences
import logging
import json
from base.models import Project
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.db.models import Q
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin
from changes.models import Category, Version
from changes.forms import CategoryForm

logger = logging.getLogger(__name__)

__author__ = 'Tim Sutton <tim@linfinit.com>'
__revision__ = '$Format:%H$'
__date__ = ''
__license__ = ''
__copyright__ = ''


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
        for category in context['categories']:
            if not first_flag:
                result += ',\n'
            result += '    "%s" : "%s"' % (category.id, category.name)
            first_flag = False
        result += '\n}'
        return result


class CategoryMixin(object):
    """Mixin class to provide standard settings for Category."""
    model = Category  # implies -> queryset = Category.objects.all()
    form_class = CategoryForm


class JSONCategoryListView(CategoryMixin, JSONResponseMixin, ListView):
    """List view for Category as json object - needed by javascript."""
    context_object_name = 'categories'

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
        return super(JSONCategoryListView, self).dispatch(
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

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which to show all versions of project.
        :rtype: QuerySet
        :raises: Http404
        """
        version_id = self.kwargs['version']
        version = get_object_or_404(Version, id=version_id)
        qs = Category.objects.all().filter(project=version.project)
        return qs


class CategoryListView(LoginRequiredMixin, CategoryMixin, ListView):
    """List view for Category."""
    context_object_name = 'categories'
    template_name = 'category/list.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['num_categories'] = context['categories'].count()
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset to show all Categories.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                try:
                    project = Project.objects.get(slug=project_slug)
                except Project.DoesNotExist:
                    raise Http404(
                        'Sorry! The project you are requesting a category for '
                        'could not be found or you do not have permission to '
                        'view the category. Try logging in as a staff member '
                        'if you wish to view it.')
                queryset = Category.objects.all().filter(
                    project=project).order_by('sort_number')
                return queryset
            else:
                raise Http404(
                        'Sorry! We could not find the project for '
                        'your category!')
        else:
            return queryset


class CategoryOrderView(LoginRequiredMixin, CategoryMixin, ListView):
    """List view to order category."""
    context_object_name = 'categories'
    template_name = 'category/order.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(CategoryOrderView, self).get_context_data(**kwargs)
        context['num_categories'] = context['categories'].count()
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset to show Categories.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                try:
                    project = Project.objects.get(slug=project_slug)
                except Project.DoesNotExist:
                    raise Http404(
                        'Sorry! The project you are requesting a category for '
                        'could not be found or you do not have permission to '
                        'view the category. Try logging in as a staff member '
                        'if you wish to view it.')
                queryset = Category.objects.all().filter(
                    Q(project=project) &
                    (Q(project__owner=self.request.user) |
                     Q(project__changelog_managers=self.request.user))
                ).order_by('sort_number').distinct()
                return queryset
            else:
                raise Http404(
                        'Sorry! We could not find the project for '
                        'your category!')
        else:
            return queryset


class CategoryDetailView(CategoryMixin, DetailView):
    """Detail view for Category."""
    context_object_name = 'category'
    template_name = 'category/detail.html'

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Category slugs are unique within a Project, we need to make
        sure that we fetch the correct Category from the correct Project

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
            try:
                project = Project.objects.get(slug=project_slug)
            except Project.DoesNotExist:
                raise Http404(
                    'The project you requested a category for does not exist.'
                )
            try:
                obj = queryset.get(project=project, slug=slug)
                return obj
            except Category.DoesNotExist:
                raise Http404(
                    'The category you requested does not exist.')
        else:
            raise Http404('Sorry! We could not find your category!')


# noinspection PyAttributeOutsideInit
class CategoryDeleteView(LoginRequiredMixin, CategoryMixin, DeleteView):
    """Delete view for Category."""
    context_object_name = 'category'
    template_name = 'category/delete.html'

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
        return super(CategoryDeleteView, self).get(request, *args, **kwargs)

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
        return super(CategoryDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the Category list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('category-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the Category objects by Project before passing to
        get_object() to ensure that we return the correct Category object.
        The requesting User must be authenticated

        :returns: Category queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """
        if not self.request.user.is_authenticated:
            raise Http404
        qs = Category.objects.filter(project=self.project)
        return qs


class CategoryOrderSubmitView(LoginRequiredMixin, CategoryMixin, UpdateView):
    """Update order view for Category."""
    context_object_name = 'category'

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
        :raises: Http404
        """
        project_slug = kwargs.get('project_slug')
        project = Project.objects.get(slug=project_slug)
        categories = Category.objects.filter(project=project)
        categories_json = request.body

        try:
            categories_request = json.loads(categories_json)
        except ValueError:
            raise Http404(
                'Error json values'
            )

        for cat in categories_request:
            category = categories.get(id=cat['id'])
            if category:
                category.sort_number = cat['sort_number']
                category.save()

        return HttpResponse('')


# noinspection PyAttributeOutsideInit
class CategoryCreateView(LoginRequiredMixin, CategoryMixin, CreateView):
    """Create view for Category."""
    context_object_name = 'category'
    template_name = 'category/create.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Category list page for the object's parent Project

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('category-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['categories'] = self.get_queryset() \
            .filter(project=self.project)
        return context

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving.

        :param form: form to validate
        :type form: CategoryForm

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect
        """
        try:
            super(CategoryCreateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                'ERROR: Category by this name already exists!')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(CategoryCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'project': self.project
        })
        return kwargs


# noinspection PyAttributeOutsideInit
class CategoryUpdateView(LoginRequiredMixin, CategoryMixin, UpdateView):
    """Update view for Category."""
    context_object_name = 'category'
    template_name = 'category/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(CategoryUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
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
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['categories'] = self.get_queryset() \
            .filter(project=self.project)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to show all projects which
        user created (staff gets all projects)
        :rtype: QuerySet
        """
        project_slug = self.kwargs.get('project_slug', None)
        project = Project.objects.get(slug=project_slug)
        qs = Category.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(
                Q(project=project) &
                (Q(project__owner=self.request.user) |
                 Q(project__changelog_managers=self.request.user)))

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the Category list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('category-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(CategoryUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Category by this name already exists!')
