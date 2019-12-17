from braces.views import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView)
from django import forms
from django.db.models import Q
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from pure_pagination.mixins import PaginationMixin
from changes.models import Sponsor
from base.models import Project


class SustainingMemberForm(forms.ModelForm):
    class Meta:
        """Meta class."""
        model = Sponsor
        fields = (
            'name',
            'contact_title',
            'sponsor_url',
            'contact_person',
            'address',
            'country',
            'sponsor_email',
            'agreement',
            'logo',
        )


class SustainingMemberCreateView(LoginRequiredMixin, CreateView):
    """Create view for sustaining member"""
    template_name = 'sustaining_member/add.html'
    model = Sponsor
    form_class = SustainingMemberForm
    form_object = None

    def get_success_url(self):
        return reverse('sponsor-list', kwargs={
            'project_slug': self.form_object.project.slug
        })

    def form_valid(self, form):
        """Check if form is valid."""
        if form.is_valid():
            self.form_object = form.save(commit=False)
            self.form_object.author = self.request.user
            self.form_object.project = Project.objects.get(
                slug=self.kwargs.get('project_slug')
            )
            self.form_object.save()
            return super(SustainingMemberCreateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SustainingMemberDetailView(LoginRequiredMixin, DetailView):
    """Detail view for sustaining member"""
    def get(self, request, *args, **kwargs):
        user = self.request.user
        try:
            sponsor = Sponsor.objects.get(
                author=user
            )
        except Sponsor.DoesNotExist:
            pass
        return HttpResponse('ok')


class SustainingMembership(LoginRequiredMixin, PaginationMixin, ListView):
    """List view of membership"""
    context_object_name = 'sustaining_members'
    template_name = 'sustaining_member/membership_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SustainingMembership, self).get_context_data(**kwargs)
        context['num_sponsors'] = context['sustaining_members'].count()
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            project = Project.objects.get(slug=project_slug)
            context['project'] = Project.objects.get(slug=project_slug)
        return context

    # noinspection PyAttributeOutsideInit
    def get_queryset(self):
        """Get the queryset for this view.
        :returns: A queryset which is filtered to only show unapproved
        Sponsor.
        :rtype: QuerySet
        :raises: Http404
        """
        user = self.request.user
        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            if self.project_slug:
                self.project = Project.objects.get(slug=self.project_slug)
                queryset = Sponsor.objects.filter(
                    author=user,
                    project=self.project)
                return queryset
            else:
                raise Http404('Sorry! We could not find '
                              'your memberships!')
        return self.queryset


# noinspection PyAttributeOutsideInit
class SustainingMemberUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sustaining_member/update.html'
    model = Sponsor
    form_class = SustainingMemberForm

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
            SustainingMemberUpdateView, self).get_context_data(**kwargs)
        context['sponsors'] = self.get_queryset() \
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
        queryset = Sponsor.objects.all()
        if self.request.user.is_staff:
            queryset = queryset
        else:
            queryset = queryset.filter(
                Q(project=self.project) &
                (Q(author=self.request.user) |
                 Q(project__owner=self.request.user) |
                 Q(project__sponsorship_managers=self.request.user)))
        return queryset

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Sponsor slugs are unique within a Project,
        we need to make sure that we fetch the correct Sponsor
        from the correct Project

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a project
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            queryset = self.get_queryset()
            member_id = self.kwargs.get('member_id', None)
            project_slug = self.kwargs.get('project_slug', None)
            if member_id and project_slug:
                project = Project.objects.get(slug=project_slug)
                obj = queryset.get(project=project, id=member_id)
                return obj
            else:
                raise Http404(
                    'Sorry! We could not find your sponsor!')

    def get_success_url(self):
        """Define the redirect URL

        After successful update of the object, the User will be redirected
        to the Sponsor list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        if self.request.GET.get('next', None):
            return self.request.GET.get('next')
        return reverse('sponsor-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check if form is valid."""
        if form.is_valid():
            self.form_object = form.save(commit=False)
            self.form_object.author = self.request.user
            self.form_object.project = Project.objects.get(
                slug=self.kwargs.get('project_slug')
            )
            self.form_object.approved = False
            self.form_object.rejected = False
            self.form_object.remarks = ''
            self.form_object.save()
            return super(SustainingMemberUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data())
