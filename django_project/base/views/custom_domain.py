# coding=utf-8
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    RedirectView)
from django.shortcuts import get_object_or_404
from pure_pagination.mixins import PaginationMixin
from base.models.custom_domain import Domain
from base.forms import RegisterDomainForm


class DomainNotFound(TemplateView):
    template_name = 'custom_domain/domain-not-found.html'


class DomainMixin(object):
    model = Domain
    form_class = RegisterDomainForm


class RegisterDomainView(LoginRequiredMixin, DomainMixin, CreateView):
    """View for domain registration."""

    context_object_name = 'domain'
    template_name = 'custom_domain/register.html'

    def get_success_url(self):
        return reverse('domain-registered')

    def get_context_data(self, **kwargs):
        context = super(RegisterDomainView, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(RegisterDomainView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class DomainThankYouView(TemplateView):
    template_name = 'custom_domain/thankyou.html'


class DomainListView(
        StaffuserRequiredMixin, DomainMixin, PaginationMixin, ListView):
    """List view for Domain."""

    context_object_name = 'domains'
    template_name = 'custom_domain/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(DomainListView, self).get_context_data(**kwargs)
        context['num_domains'] = context['domains'].count()
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
            queryset = Domain.objects.all()
            return queryset

        return self.queryset


class ApproveDomainView(StaffuserRequiredMixin, DomainMixin, RedirectView):
    """Redirect view for approving domain."""

    permanent = False
    query_string = True
    pattern_name = 'domain-list'

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

        domain_qs = \
            Domain.objects.filter(approved=False)
        domain = \
            get_object_or_404(domain_qs, pk=pk)
        domain.approved = True
        domain.save()

        return reverse(self.pattern_name)


class PendingDomainListView(
        StaffuserRequiredMixin, DomainMixin, PaginationMixin, ListView):
    """Pending list view for domain."""

    context_object_name = 'domains'
    template_name = 'custom_domain/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(PendingDomainListView, self).get_context_data(**kwargs)
        context['num_domains'] = context['domains'].count()
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
            queryset = Domain.objects.filter(approved=False)
            return queryset

        return self.queryset
