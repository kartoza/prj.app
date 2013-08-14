import logging
logger = logging.getLogger(__name__)

# noinspection PyUnresolvedReferences
import logging
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
    RedirectView,
    TemplateView)
from django.http import HttpResponseRedirect, Http404
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin

from ..models import Category, Version
from ..forms import CategoryForm


class JSONResponseMixin(object):
    """A mixin that can be used to render a JSON response.    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs)

    def convert_context_to_json(self, context):
        """Convert the context dictionary into a JSON object"""
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
    """Mixin class to provide standard settings for categories."""
    model = Category  # implies -> queryset = Entry.objects.all()
    form_class = CategoryForm


class JSONCategoryListView(CategoryMixin, JSONResponseMixin, ListView):
    context_object_name = 'categories'

    def dispatch(self, request, *args, **kwargs):
        """Ensure this view is only used via ajax."""
        if not request.is_ajax():
            raise Http404("This is an ajax view, friend.")
        return super(ListView, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_queryset(self):
        version_id = self.kwargs['version']
        version = get_object_or_404(Version, id=version_id)
        qs = Category.objects.filter(project=version.project)
        return qs


class CategoryCreateUpdateMixin(CategoryMixin, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CategoryListView(CategoryMixin, PaginationMixin, ListView):
    context_object_name = 'categories'
    template_name = 'category/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['num_categories'] = self.get_queryset().count()
        context['unapproved'] = False
        return context

    def get_queryset(self):
        qs = Category.objects.all()
        return qs


class CategoryDetailView(CategoryMixin, DetailView):
    context_object_name = 'category'
    template_name = 'category/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        qs = Category.objects.all()
        return qs

    def get_object(self, queryset=None):
        obj = super(CategoryDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class CategoryDeleteView(CategoryMixin, DeleteView):
    context_object_name = 'category'
    template_name = 'category/delete.html'

    def get_success_url(self):
        return reverse('category-list')

    def get_queryset(self):
        qs = Category.all_objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)


class CategoryCreateView(CategoryCreateUpdateMixin, CreateView):
    context_object_name = 'category'
    template_name = 'category/create.html'

    def get_success_url(self):
        return reverse('pending-category-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoryUpdateView(CategoryCreateUpdateMixin, UpdateView):
    context_object_name = 'category'
    template_name = 'category/update.html'

    def get_form_kwargs(self):
        kwargs = super(CategoryUpdateView, self).get_form_kwargs()
        return kwargs

    def get_queryset(self):
        qs = Category.objects
        return qs

    def get_success_url(self):
        return reverse('category-list')


class PendingCategoryListView(CategoryMixin, PaginationMixin, ListView):
    """List all unapproved categories"""
    context_object_name = 'categories'
    template_name = 'category/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PendingCategoryListView, self).get_context_data(**kwargs)
        context['num_categories'] = self.get_queryset().count()
        context['unapproved'] = True
        return context

    def get_queryset(self):
        qs = Category.unapproved_objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(creator=self.request.user)


class ApproveCategoryView(CategoryMixin, StaffuserRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pending-category-list'

    def get_redirect_url(self, pk):
        category_qs = Category.unapproved_objects.all()
        category = get_object_or_404(category_qs, pk=pk)
        category.approved = True
        category.save()
        return reverse(self.pattern_name)
