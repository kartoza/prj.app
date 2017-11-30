# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
import logging
import stripe
import requests
import json
from datetime import timedelta,datetime
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart, BarChart, ColumnChart

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView,
)
from collections import OrderedDict
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin
from changes.models import Version
from ..models import Project
from ..models import Merchants
from ..models import Customer
from ..models import User
from ..models import Charges
from ..forms import ProjectForm, ScreenshotFormset
from ..forms import PayForm
from vota.models import Committee, Ballot
from changes.models import SponsorshipPeriod
from certification.models import CertifyingOrganisation
from django.shortcuts import redirect

from django.http import HttpResponse
from django.shortcuts import render, redirect
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
        if self.request.user.is_authenticated():
            project = Project.objects.filter(owner=self.request.user)
            pending_organisation = CertifyingOrganisation.objects.filter(
                project=project, approved=False
            )
            context['num_project_with_pending'] = 0
            if pending_organisation:
                context['project_with_pending'] = []

                for organisation in pending_organisation:
                    if organisation.project not in \
                            context['project_with_pending']:
                        context['project_with_pending'].append(
                            organisation.project)
                        context['num_project_with_pending'] += 1
                context['message'] = \
                    'You have a pending organisation approval. '
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
    template_name = 'project/new_detail.html'

    def get_context_data(self, **kwargs):
        stripe.api_key = settings.STRIPE_KEY
        ourclientid = settings.OUR_CLIENT_ID
        myaccountid = settings.MY_ACCOUNT_ID
        user = self.request.user
        userid = 0
        projectid = self.object.id
        #Get the owner id of the project
        request = Project.objects.values_list('owner_id',flat=True).get(id=projectid)
        projectid =request
        userid = user.id
        flag=False
        if userid==projectid:
            flag=True
        username = user
        print("userid: %s" % userid)
        print("projectid: %s" % projectid)
        print("username: %s"%username)
        #Lookup username in merchant db
        merchuser = Merchants.objects.filter(firstname=username).exists()
        print("merchuser: %s"%merchuser)
        print("clientid: %s"%ourclientid)
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['projects'] = self.get_queryset()
        context['committees'] = Committee.objects.filter(project=self.object)
        context['versions'] = Version.objects.filter(
            project=self.object).order_by('-padded_version')[:5]
        context['sponsors'] = \
            SponsorshipPeriod.objects.filter(
                project=self.object).order_by('-sponsorship_level__value')
        context['screenshots'] = self.object.screenshots.all()
        context['organisations'] = \
            CertifyingOrganisation.objects.filter(
                project=self.object, approved=True)
        context['ourclientid']=ourclientid
        context['merchuser']=merchuser
        context['flag']=flag
        graphqueryset = Charges.objects.all()
        data_source = ModelDataSource(graphqueryset,fields=['date','chargeAmount'])
        chart = LineChart(data_source,options = {'title': 'Sponsorship Growth'},width=750)
        chart2 = BarChart(data_source,options = {'title': 'Sponsorship Growth'},width=750)
        chart3 = ColumnChart(data_source,options = {'title': 'Sponsorship Growth'},width=750)
        context['chart']=chart
        context['chart2']=chart2
        context['chart3']=chart3
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

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = \
                ScreenshotFormset(self.request.POST, self.request.FILES)
        else:
            context['formset'] = ScreenshotFormset()
        return context

    def form_valid(self, form):
        """Check that form and formset are valid."""
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid() and form.is_valid():
            object = form.save()
            formset.instance = object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


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

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = \
                ScreenshotFormset(
                    self.request.POST,
                    self.request.FILES,
                    instance=self.object)
        else:
            context['formset'] = ScreenshotFormset(instance=self.object)
        return context

    def get_success_url(self):
        if self.object.approved:
            return reverse('project-detail', kwargs={'slug': self.object.slug})
        else:
            return reverse('pending-project-list')

    def form_valid(self, form):
        """Check that form and formset are valid."""
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid() and form.is_valid():
            object = form.save()
            formset.instance = object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


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


@login_required
@csrf_exempt
def paymentview(request):
    '''
    :param request:
    :return:
    To do
    1. Try catch blocks
    2. Link to javascript form
    3. Add webhooks
    '''
    loggeduser = request.user.username
    stripe.api_key = settings.STRIPE_KEY
    ourclientid = settings.OUR_CLIENT_ID
    myaccountid = settings.MY_ACCOUNT_ID

    #merchantid = createmerchant(request)
    # Customer login cerdential should be unique
    #chargeid = createcharge(request,customerid,merchantid)
    try:
        dbrequest = Merchants.objects.values_list(
            'merchantid', flat=True).get(
            firstname=loggeduser)
    except BaseException:
        dbrequest = None

    returnid = request.GET.get(
        'code')
    # Payout testing
    #merchantid = "acct_1B4V9NJeuZPvjWZO"
    #balance, b = merchantpayout(merchantid)
    # platformpayout()
    context = {
        'ourclientid': ourclientid,
        'balance': balance,
        'b': b,
    }
    return render(request, 'payments/pay.html', context)


@login_required
def createaccount(request):
    context = {

    }
    return render(request, 'payments/createaccount.html', context)


@login_required
def processcustomerandcharge(request):
    firstname = request.user.username  # Look for logged in user
    customerid = 0
    merchantid = 0
    try:
        dbrequest = Customer.objects.values_list(
            'merchantid', flat=True).get(
            firstname=firstname)
    except BaseException:
        dbrequest = None

    if dbrequest is None:  # The customer does not exist
        # 1. Create user -> Click button
        return redirect(createaccount)  # Create charge and account
        # 2. Refresh processcustomerandcharge
    else:
        customerid = dbrequest
        request.session['customerid'] = customerid
        # Insert code to specify to whom the payment should go
        # Get list of projects that have connected accounts

        #1.Get list of usernames in merchant database.
        firstnames = list(Merchants.objects.values_list('firstname',flat=True))
        firstnamesid = list(User.objects.filter(username__in=firstnames).values_list('id',flat=True))
        dbmerchreq = Project.objects.filter(owner_id__in=firstnamesid).values('id','name')
        projects = Project.objects.exclude(owner_id__in=firstnamesid).values('id','name')
        lengthout = projects.count
        lengthin = dbmerchreq.count
    context = {
        'customerid': customerid,
        'merchantid': merchantid,
        'dbrequest': dbrequest,
        'dbmerchreq': dbmerchreq,
        'lengthin': lengthin,
        'lengthout': lengthout,
        'projects': projects
    }
    return render(request, 'payments/cust.html', context)


@login_required
def createmerchant(request):  # Call this method after Stripe OAuth
    merchantid = 0
    returnid = request.GET.get(
        'code')  # token that is sent to retrieve client id to be stored in db
    # POST request to OAUTH
    print("returnid: %s"%returnid)
    if returnid is not None:
        r = requests.post(
            "https://connect.stripe.com/oauth/token",
            data={
                'client_secret': stripe.api_key,
                'code': returnid,
                'grant_type': "authorization_code"})
        temp = json.loads(r.content)
        print(temp)
        if r.status_code == 200:
            print(r.status_code)
            merchantid = temp['stripe_user_id']
            firstname = request.user.username
            merchantdb = Merchants.objects.create(
                firstname=firstname, merchantid=merchantid)
            merchantdb.save()
    else:
        merchantid = "Not successfull"  # Add warning message to user
    return redirect('home')


@login_required
def createcustomer(request):
    custtok = request.form['stripeToken']
    if custtok is not None:
        customer = stripe.Customer.create(
            description="This is a customer",
            source=custtok
        )
        firstname = request.user.username
        customerid = customer.id
        customerdb = Customer.objects.create(
            firstname=firstname, merchantid=customerid)
    return customerid


@login_required
@csrf_exempt
def processview(request):
    stripe.api_key = settings.STRIPE_KEY
    myaccountid = settings.MY_ACCOUNT_ID
    custtok = request.POST.get("stripeToken")
    customer = stripe.Customer.create(
        description="This is a customer",
        source=custtok,
        stripe_account=myaccountid
    )
    firstname = request.user.username  # Get signed in userid
    customerid = customer.id
    request.session['customerid'] = customerid
    customerdb = Customer.objects.create(
        firstname=firstname, merchantid=customerid)
    context = {
        'custtok': custtok,
        'customerid': customerid
    }
    # return render(request, 'payments/cust.html', context)
    return redirect(processcustomerandcharge)


@login_required
def createcharge(request):
    # Connect the customer to the connected accounts
    # if this is a POST request we need to process the form data
    customerid = request.session.get('customerid')
    # Get the project that the payment is to be made to
    projectid = request.POST.get('projects')
    ownerid = Project.objects.values_list('owner_id',flat=True).get(id=projectid)
    error = "Unknown"
    try:
        dbrequest2 = User.objects.values_list(  # Get the username of the account holder
            'username', flat=True).get(
            id=ownerid)
    except BaseException:
        dbrequest2 = None
    try:
        dbrequest3 = Merchants.objects.values_list(  # Look up the merchant id with th username
            'merchantid', flat=True).get(
            firstname=dbrequest2)
    except BaseException:
        dbrequest3 = None
        error = "Project does not yet have account set up"
    merchantid = dbrequest3
    try:
        token = stripe.Token.create(
            customer=customerid,
            stripe_account=merchantid,
        )
        charge = stripe.Charge.create(
            amount=42000,
            currency="usd",
            source=token.id,
            application_fee=200,
            stripe_account=merchantid
        )
        # Database information for graphs
        chargestripeid = charge.id
        merchantstripeid = merchantid
        customerstripeid = customerid
        chargeAmount = (charge.amount)/100
        projectid = projectid
        userid = request.user.id
        date1 = datetime.now()
        date1 = datetime(int(2017),int(5),int(8))
        status = 1
        request.session['customerid'] = 0
        request.session['merchantid'] = 0
        storecharge = Charges.objects.create(chargestripeID=chargestripeid, merchantstripeID=merchantstripeid,
                                             customerstripeID=customerstripeid, chargeAmount=chargeAmount,
                                             projectid=projectid,
                                             userid=userid, date=date1)
        storecharge.save()
    except BaseException:
        status = 0
    if status == 1:
        return redirect('home')
    else:
        context = {
            'status': status,
        }
        return render(request, 'payments/paid.html', context)


def platformpayout():
    balance = stripe.Balance.retrieve(
        stripe_account=settings.MY_ACCOUNT_ID
    )
    for i in balance.get('available'):
        b = i.get('amount')
    payoutplatform = stripe.Payout.create(
        amount=b,
        currency='usd',
        method='instant',
        stripe_account=settings.MY_ACCOUNT_ID
    )

#Call this method when you want to tranfer available funds from Stripe to merchant bank account
def merchantpayout(merchantid):
    balance = stripe.Balance.retrieve(
        stripe_account=merchantid
    )
    for i in balance.get('available'):
        b = i.get('amount')
    '''
    payoutplatform = stripe.Payout.create(
        amount=b,
        currency='usd',
        method='instant',
        stripe_account=merchantid
    )
    '''
    return balance, b
