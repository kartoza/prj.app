import logging
logger = logging.getLogger(__name__)

# noinspection PyUnresolvedReferences
import logging
logger = logging.getLogger(__name__)

from django.core.urlresolvers import reverse

from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    TemplateView)

from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin

from .models import Project, Category, Version, Entry
from .forms import ProjectForm, CategoryForm, VersionForm, EntryForm


class ProjectMixin(object):
    model = Project  # implies -> queryset = Entry.objects.all()
    form_class = ProjectForm


class ProjectCreateUpdateMixin(ProjectMixin, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProjectListView(ProjectMixin, PaginationMixin, ListView):
    context_object_name = 'projects'
    template_name = 'project/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['num_projects'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        projects_qs = Project.objects.all()
        return projects_qs


class ProjectDetailView(ProjectMixin, DetailView):
    context_object_name = 'project'
    template_name = 'project/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        projects_qs = Project.objects.all()
        return projects_qs

    def get_object(self, queryset=None):
        obj = super(ProjectDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class ProjectDeleteView(ProjectMixin, DeleteView):
    context_object_name = 'project'
    template_name = 'project/delete.html'

    def get_success_url(self):
        return reverse('project-list')


class ProjectCreateView(ProjectCreateUpdateMixin, CreateView):
    context_object_name = 'project'
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdateView(ProjectCreateUpdateMixin, UpdateView):
    context_object_name = 'project'
    template_name = 'project/update.html'

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        return kwargs

    def get_queryset(self):
        projects_qs = Project.objects
        return projects_qs

    def get_success_url(self):
        return reverse('project-detail')

# Category management


class CategoryMixin(object):
    model = Category  # implies -> queryset = Entry.objects.all()
    form_class = CategoryForm


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
        return context

    def get_queryset(self):
        categories_qs = Category.objects.all()
        return categories_qs


class CategoryDetailView(CategoryMixin, DetailView):
    context_object_name = 'category'
    template_name = 'category/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        categories_qs = Category.objects.all()
        return categories_qs

    def get_object(self, queryset=None):
        obj = super(CategoryDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class CategoryDeleteView(CategoryMixin, DeleteView):
    context_object_name = 'category'
    template_name = 'category/delete.html'

    def get_success_url(self):
        return reverse('category-list')


class CategoryCreateView(CategoryCreateUpdateMixin, CreateView):
    context_object_name = 'category'
    template_name = 'category/create.html'

    def get_success_url(self):
        return reverse('category-list')

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
        categories_qs = Category.objects
        return categories_qs

    def get_success_url(self):
        return reverse('category-list')


# Version management


class VersionMixin(object):
    model = Version  # implies -> queryset = Entry.objects.all()
    form_class = VersionForm


class VersionCreateUpdateMixin(VersionMixin, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(VersionMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class VersionListView(VersionMixin, PaginationMixin, ListView):
    context_object_name = 'versions'
    template_name = 'version/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(VersionListView, self).get_context_data(**kwargs)
        context['num_versions'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        versions_qs = Version.objects.all()
        return versions_qs


class VersionDetailView(VersionMixin, DetailView):
    context_object_name = 'version'
    template_name = 'version/detail.html'

    def get_context_data(self, **kwargs):
        context = super(VersionDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        versions_qs = Version.objects.all()
        return versions_qs

    def get_object(self, queryset=None):
        obj = super(VersionDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class VersionDeleteView(VersionMixin, DeleteView):
    context_object_name = 'version'
    template_name = 'version/delete.html'

    def get_success_url(self):
        return reverse('version-list')


class VersionCreateView(VersionCreateUpdateMixin, CreateView):
    context_object_name = 'version'
    template_name = 'version/create.html'

    def get_success_url(self):
        return reverse('version-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class VersionUpdateView(VersionCreateUpdateMixin, UpdateView):
    context_object_name = 'version'
    template_name = 'version/update.html'

    def get_form_kwargs(self):
        kwargs = super(VersionUpdateView, self).get_form_kwargs()
        return kwargs

    def get_queryset(self):
        versions_qs = Version.objects
        return versions_qs

    def get_success_url(self):
        return reverse('version-list')


# Changelog entries

class EntryMixin(object):
    model = Entry  # implies -> queryset = Entry.objects.all()
    form_class = EntryForm


class EntryCreateUpdateMixin(EntryMixin, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(EntryMixin, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class EntryListView(EntryMixin, PaginationMixin, ListView):
    context_object_name = 'entries'
    template_name = 'entry/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        context['num_entries'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        entries_qs = Entry.objects.all()
        return entries_qs


class EntryDetailView(EntryMixin, DetailView):
    context_object_name = 'entry'
    template_name = 'entry/detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        entries_qs = Entry.objects.all()
        return entries_qs

    def get_object(self, queryset=None):
        obj = super(EntryDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class EntryDeleteView(EntryMixin, DeleteView):
    context_object_name = 'entry'
    template_name = 'entry/delete.html'

    def get_success_url(self):
        return reverse('entry-list')


class EntryCreateView(EntryCreateUpdateMixin, CreateView):
    context_object_name = 'entry'
    template_name = 'entry/create.html'

    def get_success_url(self):
        return reverse('entry-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class EntryUpdateView(EntryCreateUpdateMixin, UpdateView):
    context_object_name = 'entry'
    template_name = 'entry/update.html'

    def get_form_kwargs(self):
        kwargs = super(EntryUpdateView, self).get_form_kwargs()
        return kwargs

    def get_queryset(self):
        entries_qs = Entry.objects
        return entries_qs

    def get_success_url(self):
        return reverse('entry-list')
