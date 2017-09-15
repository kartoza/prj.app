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
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView,
)
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin
from changes.models import Version
from ..models import Project
<<<<<<< HEAD
from ..forms import ProjectForm, ScreenshotFormset
=======
from ..models import Merchants
from ..models import Customer
from ..forms import ProjectForm
from ..forms import PayForm
>>>>>>> stripe progress
from vota.models import Committee, Ballot
from changes.models import SponsorshipPeriod
from certification.models import CertifyingOrganisation
from django.conf import settings
<<<<<<< HEAD
from django.shortcuts import redirect

=======
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
>>>>>>> Developing connect platform WIP
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
    stripe.api_key = "sk_test_OHW7bvLJhDtm1k2pI8AwIiEY"
    ourclientid = "ca_BM5OIMXOFqSOBjJcr4DrGHTsK3tLFuW3"
    myaccount = stripe.Account.retrieve("acct_1AzNDQGz66mVbJVl")
    myaccountid = myaccount.id

    merchantid = createmerchant(request)
    # Customer login cerdential should be unique

    fields = "fields"

    #chargeid = createcharge(request,customerid,merchantid)
    returnid = request.GET.get(
        'code')
    context = {
        # "charge":charge,
        # "chargeid":chargeid,
        "ourclientid": ourclientid,
        "merchantid": merchantid,
        "myaccount": myaccount,
        "returnid": returnid,
        "fields": fields,
    }
    return render(request, 'payments/pay.html', context)


def createaccount(request):
    context = {

    }
    return render(request, 'payments/createaccount.html', context)


def processcustomerandcharge(request):
    firstname = "testcustomerfinal4"  # Look for logged in user
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
        # Get list of merchants
        dbmerchreq = Merchants.objects.values('merchantid', 'firstname')
        length = dbmerchreq.count
        merchantid = "acct_1B1rtDBWHazZ6NrT"  # value must be taken from form
        request.session['merchantid'] = merchantid
    context = {
        'customerid': customerid,
        'merchantid': merchantid,
        'dbrequest': dbrequest,
        'dbmerchreq': dbmerchreq,
        'length': length,
    }
    return render(request, 'payments/cust.html', context)


def createmerchant(request):  # Call this method after Stripe OAuth
    returnid = request.GET.get(
        'code')  # token that is sent to retrieve client id to be stored in db
    # POST request to OAUTH
    if returnid is not None:
        r = requests.post(
            "https://connect.stripe.com/oauth/token",
            data={
                'client_secret': stripe.api_key,
                'code': returnid,
                'grant_type': "authorization_code"})
        temp = json.loads(r.content)
        if r.status_code == 200:
            merchantid = temp['stripe_user_id']
        # Hard coded clientid returned- acct_1B1rtDBWHazZ6NrT
        else:
            merchantid = "acct_1B1rtDBWHazZ6NrT"
        firstname = "testmerchant"
        merchantdb = Merchants.objects.create(
            firstname=firstname, merchantid=merchantid)
        merchantdb.save()
    else:
        merchantid = "acct_1B1rtDBWHazZ6NrT"
    return merchantid


def createcustomer(request):
    custtok = request.form['stripeToken']
    if custtok is not None:
        customer = stripe.Customer.create(
            description="This is a customer",
            source=custtok
        )
        firstname = "testcustomer"
        customerid = customer.id
        customerdb = Customer.objects.create(
            firstname=firstname, merchantid=customerid)
    return customerid


@csrf_exempt
def processview(request):
    stripe.api_key = "sk_test_OHW7bvLJhDtm1k2pI8AwIiEY"
    myaccount = stripe.Account.retrieve("acct_1AzNDQGz66mVbJVl")
    myaccountid = myaccount.id
    custtok = request.POST.get("stripeToken")
    customer = stripe.Customer.create(
        description="This is a customer",
        source=custtok,
        stripe_account=myaccountid
    )
    firstname = "testcustomerfinal4"  # Get signed in userid
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


def createcharge(request):
    # Connect the customer to the connected accounts
    # if this is a POST request we need to process the form data
    #customerid = "cus_BP643ue5uueqr1"
    customerid = request.session.get('customerid')
    merchantid = request.POST.get('merchants')
    status = "not paid"
    if customerid is not None and merchantid is not None:
        token = stripe.Token.create(
            customer=customerid,
            stripe_account=merchantid,
        )

        charge = stripe.Charge.create(
            amount=68000,
            currency="usd",
            source=token.id,
            application_fee=200,
            stripe_account=merchantid
        )
        status = "paid"
        request.session['customerid'] = 0
        request.session['merchantid'] = 0

    context = {
        'status': status,
        'merchantid': merchantid,
        'customerid': customerid
    }
    return render(request, 'payments/paid.html', context)


def platformpayout():
    platformbalance = stripe.Balance.retrieve(
        stripe_account=myaccountid
    )
    payoutplatform = stripe.Payout.create(
        amount=platformamount,
        currency='usd',
        stripe_account=myaccountid
    )


def merchantpayout():
    merchantbalance = stripe.Balance.retrieve(
        stripe_account=merchantid
    )
    payoutmerchant = stripe.Payout.create(
        amount=800,
        currency='usd',
        method='instant',
        stripe_account=merchantid
    )
