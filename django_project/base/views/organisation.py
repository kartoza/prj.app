# coding=utf-8
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import (
    CreateView,
    ListView,
    RedirectView,
    DeleteView,
    UpdateView)
from django.shortcuts import get_object_or_404
from pure_pagination.mixins import PaginationMixin
from base.models import Organisation
from base.forms import OrganisationForm


class OrganisationMixin(object):
    model = Organisation
    form_class = OrganisationForm


class CreateOrganisationView(
        LoginRequiredMixin, OrganisationMixin, CreateView):
    """Create view for organisation."""

    context_object_name = 'organisation'
    template_name = 'organisation/create.html'

    def get_success_url(self):
        return reverse('list-organisation')

    def get_context_data(self, **kwargs):
        context = super(
            CreateOrganisationView, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateOrganisationView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class OrganisationListView(OrganisationMixin, PaginationMixin, ListView):
    """List view for organisation."""

    context_object_name = 'organisations'
    template_name = 'organisation/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(OrganisationListView, self).get_context_data(**kwargs)
        context['num_organisations'] = context['organisations'].count()
        context['unapproved'] = False
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
            queryset = Organisation.objects.all()
            return queryset

        return self.queryset


class ApproveOrganisationView(
        StaffuserRequiredMixin, OrganisationMixin, RedirectView):
    """Redirect view for approving organisation."""

    permanent = False
    query_string = True
    pattern_name = 'list-organisation'

    def get_redirect_url(self, pk):
        """Save Certifying Organisation as approved and redirect.

        :param project_slug: The slug of the parent
                            Certifying Organisation's parent Project.
        :type project_slug: str

        :param slug: The slug of the Certifying Organisation.
        :type slug: str

        :returns: URL
        :rtype: str
        """

        organisation_qs = \
            Organisation.objects.filter(approved=False)
        organisation = \
            get_object_or_404(organisation_qs, pk=pk)
        organisation.approved = True
        organisation.save()

        return reverse(self.pattern_name)


class PendingOrganisationListView(
        OrganisationMixin, PaginationMixin, ListView):
    """List view for pending organisation."""

    context_object_name = 'organisations'
    template_name = 'organisation/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            PendingOrganisationListView, self).get_context_data(**kwargs)
        context['num_organisations'] = context['organisations'].count()
        context['unapproved'] = True
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
            queryset = Organisation.objects.filter(approved=False)
            return queryset

        return self.queryset


class OrganisationDeleteView(
        StaffuserRequiredMixin, OrganisationMixin, DeleteView):
    context_object_name = 'organisation'
    template_name = 'organisation/delete.html'

    def get_success_url(self):
        return reverse('list-organisation')

    def get_queryset(self):
        qs = Organisation.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            raise Http404


class OrganisationUpdateView(
        LoginRequiredMixin, OrganisationMixin, UpdateView):
    context_object_name = 'organisation'
    template_name = 'organisation/update.html'

    def get_form_kwargs(self):
        kwargs = super(OrganisationUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_queryset(self):
        qs = Organisation.objects
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(owner=self.request.user)

    def get_success_url(self):
        if self.object.approved:
            return reverse('list-organisation')
        else:
            return reverse('pending-list-organisation')
