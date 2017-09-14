# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
import logging
import stripe
import requests
import json
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView,
)
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin
from changes.models import Version
from ..models import Project
from ..forms import ProjectForm
from vota.models import Committee, Ballot
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
logger = logging.getLogger(__name__)


class ProjectMixin(object):
    model = Project
    form_class = ProjectForm


class ProjectBallotListView(ProjectMixin, PaginationMixin, DetailView):
    """List all ballots within in a project"""
    context_object_name = 'project'
    template_name = 'project/ballot-list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        context = super(
            ProjectBallotListView, self).get_context_data(**kwargs)
        committees = Committee.objects.filter(project=self.object)
        ballots = []
        for committee in committees:
            if self.request.user.is_authenticated and \
                    self.request.user in committee.users.all():
                    committee_ballots = Ballot.objects.filter(
                        committee=committee)
            else:
                committee_ballots = Ballot.objects.filter(
                    committee=committee).filter(private=False)
            if committee_ballots:
                ballots.append(committee_ballots)
        context['ballots_list'] = ballots
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated():
            projects_qs = Project.approved_objects.all()
        else:
            projects_qs = Project.public_objects.all()
        return projects_qs


class ProjectListView(ProjectMixin, PaginationMixin, ListView):
    """List all approved projects"""
    context_object_name = 'projects'
    template_name = 'project/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Add to the view's context data

        :param kwargs: (django dictionary)
        :type kwargs: dict

        :return: context
        :rtype: dict

        """
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['num_projects'] = self.get_queryset().count()
        context[
            'PROJECT_VERSION_LIST_SIZE'] = settings.PROJECT_VERSION_LIST_SIZE
        return context

    def get_queryset(self):
        """Specify the queryset

        Return a specific queryset based on the requesting user's status

        :return: If user.is_authenticated: All approved projects
            If not user.is_authenticated: All public projects
        :rtype: QuerySet

        """
        if self.request.user.is_authenticated():
            projects_qs = Project.approved_objects.all()
        else:
            projects_qs = Project.public_objects.all()
        return projects_qs


class ProjectDetailView(ProjectMixin, DetailView):
    context_object_name = 'project'
    template_name = 'project/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['projects'] = self.get_queryset()
        context['committees'] = Committee.objects.filter(project=self.object)
        page_size = settings.PROJECT_VERSION_LIST_SIZE
        context['versions'] = Version.objects.filter(
            project=self.object).order_by('-padded_version')[:page_size]
        return context

    def get_queryset(self):
        projects_qs = Project.approved_objects.all()
        return projects_qs

    def get_object(self, queryset=None):
        obj = super(ProjectDetailView, self).get_object(queryset)
        obj.request_user = self.request.user
        return obj


class ProjectDeleteView(LoginRequiredMixin, ProjectMixin, DeleteView):
    context_object_name = 'project'
    template_name = 'project/delete.html'

    def get_success_url(self):
        return reverse('project-list')

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise Http404

        qs = Project.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(owner=self.request.user)


class ProjectCreateView(LoginRequiredMixin, ProjectMixin, CreateView):
    context_object_name = 'project'
    template_name = 'project/create.html'

    def get_success_url(self):
        return reverse('pending-project-list')

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(ProjectCreateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Project by this name already exists!')


class ProjectUpdateView(LoginRequiredMixin, ProjectMixin, UpdateView):
    context_object_name = 'project'
    template_name = 'project/update.html'

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_queryset(self):
        qs = Project.objects
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(owner=self.request.user)

    def get_success_url(self):
        if self.object.approved:
            return reverse('project-detail', kwargs={'slug': self.object.slug})
        else:
            return reverse('pending-project-list')

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(ProjectUpdateView, self).form_valid(form)
        except IntegrityError:
            raise ValidationError(
                'ERROR: Version by this name already exists!')


class PendingProjectListView(
        ProjectMixin,
        PaginationMixin,
        ListView,
        StaffuserRequiredMixin,
        LoginRequiredMixin):
    """List all users unapproved projects - staff users see all unapproved."""
    context_object_name = 'projects'
    template_name = 'project/list.html'
    paginate_by = settings.PROJECT_VERSION_LIST_SIZE

    def get_queryset(self):
        projects_qs = Project.unapproved_objects.all()
        if self.request.user.is_staff:
            return projects_qs
        else:
            try:
                return projects_qs.filter(owner=self.request.user)
            except TypeError:
                # LoginRequiredMixin should really be catching this...
                raise Http404('You must be logged in to see pending projects.')

    def get_context_data(self, **kwargs):
        context = super(
            PendingProjectListView, self).get_context_data(**kwargs)
        context['num_projects'] = self.get_queryset().count()
        context['unapproved'] = True
        return context


class ApproveProjectView(StaffuserRequiredMixin, ProjectMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pending-project-list'

    def get_redirect_url(self, slug):
        projects_qs = Project.unapproved_objects.all()
        project = get_object_or_404(projects_qs, slug=slug)
        project.approved = True
        project.save()
        return reverse(self.pattern_name)

def paymentview(request):
    '''
    :param request:
    :return:
    To do
    1. Try catch blocks
    2. Link to javascript form
    3. Add webhooks
    '''
    stripe.api_key = "sk_test_OHW7bvLJhDtm1k2pI8AwIiEY"
    ourclientid =  "ca_BM5OIMXOFqSOBjJcr4DrGHTsK3tLFuW3"
    myaccount = stripe.Account.retrieve("acct_1AzNDQGz66mVbJVl")
    myaccountid = myaccount.id
    '''
        Stripe connect
    '''
    returnid = request.GET.get('code') #token that is sent to retrieve client id to be stored in db
    #POST request to OAUTH
    
    r = requests.post("https://connect.stripe.com/oauth/token", data={'client_secret':stripe.api_key,'code':returnid,'grant_type':"authorization_code"})
    temp = json.loads(r.content)
    if r.status_code==200:
        merchantid = temp['stripe_user_id']
    #Hard coded clientid returned- acct_1B1rtDBWHazZ6NrT
    else:
        merchantid = "acct_1B1rtDBWHazZ6NrT"

    #1. View account balances of platform and connected account and card
    merchantbalance = stripe.Balance.retrieve(
        stripe_account=merchantid
    )
    #clientamount = clientbalance.amount
    platformbalance = stripe.Balance.retrieve(
        stripe_account=myaccountid
    )
    #platformamount = platformbalance.amount
    #3. Customer account info
    custtok =stripe.Token.create(
        bank_account={
            "country": 'US',
            "currency": 'usd',
            "account_holder_name": 'Avery White',
            "account_holder_type": 'individual',
            "routing_number": '110000000',
            "account_number": '000123456789'
        },
    )
    customer = stripe.Customer.create(
        description="This is a customer",
        source=custtok
    )
    customerid = customer.id #Store to update info
    #2. Process a charge
    charge = stripe.Charge.create(
        amount=500,
        currency="usd",
        source="tok_visa",
        application_fee=200,
        stripe_account=merchantid
    )
    chargeid = charge.id
    #3. View account balances again


    #4. Create payout - Merchant
    payoutclient = stripe.Payout.create(
        amount=800,
        currency='usd',
        method='instant',
        stripe_account=merchantid
    )
    #5. Create a payout - Platform
    '''
    payoutplatform = stripe.Payout.create(
        amount=platformamount,
        currency='usd',
        stripe_account=myaccountid
    )
    '''
    context = {
        #"charge":charge,
        #"chargeid":chargeid,
        "ourclientid":ourclientid,
        "returnid":returnid,
        "merchantid":merchantid,
        "merchantbalance":merchantbalance,
        "platformbalance":platformbalance,
        "myaccount":myaccount,
        "customer":customer,
        "r":r
    }
    return render(request,'payments/pay.html',context)


