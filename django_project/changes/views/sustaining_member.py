from datetime import date, timedelta, datetime
import ast
import stripe
import djstripe.models
import djstripe.settings
from braces.views import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView)
from django import forms
from django.db.models import Q, Case, When, BooleanField
from django.http import HttpResponseRedirect, Http404
from changes.models import Sponsor, SponsorshipPeriod, SponsorshipLevel
from base.models import Project
from changes.models import active_sustaining_membership
from changes.forms import SustainingMemberPeriodForm
from changes import (
    NOTICE_SUSTAINING_MEMBER_CREATED,
    NOTICE_SUSTAINING_MEMBER_UPDATED,
    NOTICE_SUBSCRIPTION_UPDATED,
    NOTICE_SUBSCRIPTION_CREATED
)
from helpers.notification import send_notification


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
            'logo',
        )


class SustainingMemberPeriodStripeMixin(object):
    object = None
    request = None

    def stripe_metadata(self):
        """Returns a metadata dict for stripe"""
        return {
            'start_date': str(self.object.start_date),
            'end_date': str(self.object.end_date),
            'project_id': self.object.project.id,
            'sustaining_member_id': self.object.sponsor.id,
            'sustaining_member_name': self.object.sponsor.name,
            'user_id': self.request.user.id,
            'recurring': self.object.recurring,
            'server_time': datetime.now().ctime()
        }


class SustainingMemberCreateView(LoginRequiredMixin, CreateView):
    """Create view for sustaining member"""
    template_name = 'sustaining_member/add.html'
    model = Sponsor
    form_class = SustainingMemberForm
    form_object = None

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(
            slug=self.kwargs.get('project_slug')
        )
        active_memberships = active_sustaining_membership(
            self.request.user,
            project
        )
        if active_memberships.exists():
            return redirect(reverse(
                'sustaining-membership', kwargs={
                    'project_slug': self.kwargs.get('project_slug')
                }
            ))
        return super(SustainingMemberCreateView, self).get(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(SustainingMemberCreateView, self).get_context_data(
            **kwargs
        )
        context['the_project'] = Project.objects.get(
            slug=self.kwargs.get('project_slug')
        )
        return context

    def get_success_url(self):
        return reverse('sustaining-membership', kwargs={
            'project_slug': self.form_object.project.slug
        })

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def send_notification(self, sustaining_member, sponsorship_managers):
        """Send a notification to author and managers"""
        send_notification(
            users=[
                      self.request.user,
                  ] + list(sponsorship_managers),
            label=NOTICE_SUSTAINING_MEMBER_CREATED,
            extra_context={
                'sustaining_member': sustaining_member,
                'sustaining_member_manager': sponsorship_managers[0],
                'active_site': self.request.get_host()
            },
            request_user=self.request.user
        )

    def form_valid(self, form):
        """Check if form is valid."""
        if form.is_valid():
            project = Project.objects.get(
                slug=self.kwargs.get('project_slug')
            )
            self.form_object = form.save(commit=False)
            self.form_object.author = self.request.user
            self.form_object.project = project
            self.form_object.sustaining_membership = True
            self.form_object.save()
            sponsorship_managers = project.sponsorship_managers.all().exclude(
                id=self.request.user.id
            )
            # Send a notification
            self.send_notification(self.form_object,
                                   list(sponsorship_managers))

            return super(SustainingMemberCreateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SustainingMembership(LoginRequiredMixin, DetailView):
    """Detail view of membership"""
    context_object_name = 'sustaining_member'
    template_name = 'sustaining_member/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SustainingMembership, self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        sustaining_member = self.get_object()
        today = date.today()
        next_month = today + timedelta(days=30)
        try:
            context['subscription'] = SponsorshipPeriod.objects.filter(
                project__slug=project_slug,
                sponsor=sustaining_member
            ).annotate(
                active_period=Case(
                    When(Q(end_date__gt=today) | Q(recurring=True), then=True),
                    default=False,
                    output_field=BooleanField()
                ),
                expiring=Case(
                    When(Q(end_date__lt=next_month) & Q(recurring=False),
                         then=True),
                    default=False,
                    output_field=BooleanField()
                )
            )[0]
        except IndexError:
            context['subscription'] = None
        just_approved = (
                sustaining_member.approved and
                not SponsorshipPeriod.objects.filter(
                    sponsor=sustaining_member,
                    project__slug=project_slug
                ).exists()
        )
        if project_slug:
            context['project'] = Project.objects.get(slug=project_slug)
        context['just_approved'] = just_approved
        return context

    def get_object(self, queryset=None):
        """Return the a Sustaining Membership object.
        It must match with project_slug and the user"""
        try:
            project_slug = self.kwargs.get('project_slug', None)
            project = Project.objects.get(slug=project_slug)
            sustaining_member = get_object_or_404(
                Sponsor,
                project=project,
                author=self.request.user,
                sustaining_membership=True,
                active=True
            )
            return sustaining_member
        except (Http404, Sponsor.MultipleObjectsReturned):
            return None


# noinspection PyAttributeOutsideInit
class SustainingMemberUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sustaining_member/update.html'
    model = Sponsor
    form_class = SustainingMemberForm

    def get(self, request, *args, **kwargs):
        sustaining_member = self.get_object()
        if not sustaining_member.approved and not sustaining_member.rejected:
            raise Http404('Editing this data is not allowed')
        return super(SustainingMemberUpdateView, self).get(
            request, *args, **kwargs
        )

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
                obj = queryset.filter(
                    project=project, id=member_id, sustaining_membership=True)
                return obj[obj.count() - 1]
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
        return reverse('sustaining-membership', kwargs={
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
            sponsorship_managers = (
                   self.form_object.project.sponsorship_managers.all().exclude(
                       id=self.request.user.id
                   )
            )
            if not self.form_object.approved:
                self.form_object.rejected = False
                self.form_object.remarks = ''

            send_notification(
                users=[
                          self.request.user,
                      ] + list(sponsorship_managers),
                label=NOTICE_SUSTAINING_MEMBER_UPDATED,
                extra_context={
                    'sustaining_member': self.form_object,
                    'active_site': self.request.get_host()
                },
                request_user=self.request.user
            )

            self.form_object.save()
            return super(SustainingMemberUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data())


# noinspection PyAttributeOutsideInit
class SustainingMemberPeriodCreateView(
        LoginRequiredMixin,
        CreateView,
        SustainingMemberPeriodStripeMixin):
    """Create view for Sponsorship Period."""
    context_object_name = 'sustaining_member_period'
    template_name = 'sustaining_membership/create.html'
    model = SponsorshipPeriod
    form_class = SustainingMemberPeriodForm

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to membership view

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('sustaining-membership', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
                SustainingMemberPeriodCreateView,
                self).get_context_data(**kwargs)

        if djstripe.models.Plan.objects.count() == 0:
            raise Exception(
                "No Product Plans in the dj-stripe database - "
                "create some in your "
                "stripe account and then "
                "run `./manage.py djstripe_sync_plans_from_stripe` "
                "(or use the dj-stripe webhooks)"
            )

        project_slug = self.kwargs.get('project_slug', None)
        project = Project.objects.get(slug=project_slug)
        member_id = self.kwargs.get('member_id', None)
        member = Sponsor.objects.get(id=member_id)
        today_date = date.today()

        context['sponsorship_period'] = (
            self.get_queryset().filter(project=project))
        context['sponsorhip_levels'] = (
            SponsorshipLevel.objects.filter(
                project=project
            )
        )
        context['default_period'] = 1
        context['project'] = project
        context['date_start'] = today_date.strftime("%B %d, %Y")
        context['date_end'] = today_date.replace(
            year = today_date.year + 1).strftime("%B %d, %Y")
        context['member'] = member

        if not member.approved:
            raise Http404('Sustaining Member is not approved')
        try:
            period = SponsorshipPeriod.objects.get(
                sponsor=member,
                project=project
            )
            if ((period.end_date and period.end_date > date.today()) or
                    period.recurring):
                raise Http404('Period already exist')
        except SponsorshipPeriod.DoesNotExist:
            pass

        return context

    def process_payment(self,
                        stripe_source_id, plan_id, recurring,
                        date_end, period_year, metadata=None):
        """Process payment from stripe."""

        # Create the stripe Customer, by default subscriber Model is User,
        # this can be overridden with settings.DJSTRIPE_SUBSCRIBER_MODEL
        customer, created = djstripe.models.Customer.get_or_create(
            subscriber=self.request.user)

        if not metadata:
            metadata = {}

        # Add the source as the customer's default card
        customer.add_card(stripe_source_id)

        optional = {}
        optional['metadata'] = metadata

        if recurring:
            optional['cancel_at_period_end'] = False
        else:
            if period_year > 1:
                optional['cancel_at'] = int(date_end.timestamp())
            else:
                optional['cancel_at_period_end'] = True

        # Using the Stripe API, create a subscription for this customer,
        # using the customer's default payment source
        stripe_subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"plan": plan_id}],
            billing="charge_automatically",
            api_key=djstripe.settings.STRIPE_SECRET_KEY,
            **optional
        )

        # Sync the Stripe API return data to the database,
        # this way we don't need to wait for a webhook-triggered sync
        subscription = djstripe.models.Subscription.sync_from_stripe_data(
            stripe_subscription
        )
        self.request.subscription = subscription
        return subscription

    def form_valid(self, form):
        """Save new created Sponsor

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect
        """
        member_id = self.kwargs.get('member_id', None)
        project_slug = self.kwargs.get('project_slug', None)
        source_id = self.request.POST.get('stripe-source-id')
        sponsor = Sponsor.objects.get(id=member_id)
        if not sponsor.approved:
            raise Http404('Sponsor is not approved')
        try:
            recurring = ast.literal_eval(
                self.request.POST.get('recurring').capitalize()
            )
        except ValueError:
            recurring = False

        self.object = form.save(commit=False)
        plan_id = self.object.sponsorship_level.subscription_plan.id
        try:
            period_end = int(self.request.POST.get('period-end', None))
        except (ValueError, TypeError):
            period_end = 1
        self.object.end_date = self.object.start_date.replace(
            year=self.object.start_date.year + period_end)
        self.object.author = self.request.user
        self.object.sponsor = sponsor
        self.object.project = Project.objects.get(slug=project_slug)
        self.object.approved = True
        if recurring:
            self.object.recurring = True
        sponsorship_managers = self.object.project.sponsorship_managers.all()
        self.object.save()

        # Kick off the stripe payment
        subscription = self.process_payment(
            source_id,
            plan_id,
            recurring,
            self.object.end_date,
            period_end,
            self.stripe_metadata())
        if subscription:
            self.object.subscription = subscription
            # Send a notification
            send_notification(
                [
                    self.request.user,
                ] + list(sponsorship_managers),
                NOTICE_SUBSCRIPTION_CREATED,
                {
                    'sustaining_member': self.object.sponsor.name,
                    'sustaining_member_level': self.object.sponsorship_level,
                    'author': self.request.user,
                    'recurring': 'Yes' if recurring else 'No',
                    'date_start': self.object.start_date.strftime(
                        "%B %d, %Y"),
                    'date_end': self.object.end_date.strftime(
                        "%B %d, %Y"),
                    'active_site': self.request.get_host()
                })
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# noinspection PyAttributeOutsideInit
class SustainingMemberPeriodUpdateView(
        LoginRequiredMixin,
        UpdateView,
        SustainingMemberPeriodStripeMixin):
    """Create view for Sponsorship Period."""
    context_object_name = 'sustaining_member_period'
    template_name = 'sustaining_membership/update.html'
    model = SponsorshipPeriod
    form_class = SustainingMemberPeriodForm

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to membership view

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('sustaining-membership', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
                SustainingMemberPeriodUpdateView,
                self).get_context_data(**kwargs)

        project_slug = self.kwargs.get('project_slug', None)
        project = Project.objects.get(slug=project_slug)
        member_id = self.kwargs.get('member_id', None)
        member = Sponsor.objects.get(id=member_id)
        period = SponsorshipPeriod.objects.get(
            sponsor=member,
            project=project
        )

        context['project'] = project
        context['date_start'] = period.start_date.strftime("%B %d, %Y")
        context['min_period'] = (
            date.today().year - period.start_date.year if
            date.today().year > period.start_date.year else
            1
        )
        if period.end_date:
            context['date_end'] = period.end_date.strftime("%B %d, %Y")
            context['period_year'] = (
                    period.end_date.year - period.start_date.year
            )
        else:
            context['period_year'] = 1
        context['member'] = member
        context['recurring'] = period.recurring
        context['level'] = period.sponsorship_level

        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        projects which user created (staff gets all projects)
        :rtype: QuerySet
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        qs = SponsorshipPeriod.objects.all()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(
                Q(project=self.project) & (
                    Q(author=self.request.user) | (
                        Q(project__owner=self.request.user)) | (
                        Q(project__sponsorship_managers=self.request.user))))

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
                obj = queryset.get(
                    project=project,
                    sponsor__id=member_id,
                    sponsor__sustaining_membership=True)
                return obj
            else:
                raise Http404(
                    'Sorry! We could not find your sponsor!')

    def update_subscription(self, subscription, recurring, period_end,
                            metadata=None):
        """Update subscription in stripe"""
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
        optional = {}
        if not metadata:
            metadata = {}

        optional['metadata'] = metadata
        if recurring:
            optional['cancel_at_period_end'] = False
        else:
            if period_end > 1:
                new_period_end = subscription.current_period_start.replace(
                    year=subscription.current_period_start.year + period_end)
                if new_period_end != subscription.current_period_end:
                    period_end_timestamp = new_period_end.timestamp()
                else:
                    period_end_timestamp = (
                        subscription.current_period_end.timestamp()
                    )
                optional['cancel_at'] = int(period_end_timestamp)
            else:
                optional['cancel_at_period_end'] = True

        stripe_subscription = stripe.Subscription.modify(
            subscription.id,
            **optional
        )
        return djstripe.models.Subscription.sync_from_stripe_data(
            stripe_subscription
        )

    def form_valid(self, form):
        """Save update period

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect
        """
        self.object = form.save(commit=False)
        try:
            recurring = ast.literal_eval(
                self.request.POST.get('recurring').capitalize()
            )
        except ValueError:
            recurring = False
        try:
            period_end = int(self.request.POST.get('period-end', None))
        except ValueError:
            period_end = None
        self.object.recurring = recurring
        if not period_end:
            period_end = 1
        self.object.end_date = self.object.start_date.replace(
            year=self.object.start_date.year + period_end)

        subscription = self.update_subscription(
            self.object.subscription,
            recurring,
            period_end,
            self.stripe_metadata()
        )
        if subscription:
            project = Project.objects.get(
                slug=self.kwargs.get('project_slug')
            )
            sponsorship_managers = project.sponsorship_managers.all()
            # Send a notification
            send_notification(
                users=[
                          self.request.user,
                      ] + list(sponsorship_managers),
                label=NOTICE_SUBSCRIPTION_UPDATED,
                extra_context={
                    'the_project_slug': self.kwargs.get('project_slug'),
                    'sustaining_member': self.object.sponsor.name,
                    'sustaining_member_level': self.object.sponsorship_level,
                    'author': self.request.user,
                    'recurring': 'Yes' if recurring else 'No',
                    'date_start': self.object.start_date.strftime(
                        "%B %d, %Y"),
                    'date_end': self.object.start_date.replace(
                        year=self.object.start_date.year + period_end
                    ).strftime(
                        "%B %d, %Y"),
                    'active_site': self.request.get_host()
                },
                request_user=self.request.user
            )
            self.object.save()
        else:
            raise Http404('Subscription could not be updated')
        return HttpResponseRedirect(self.get_success_url())
