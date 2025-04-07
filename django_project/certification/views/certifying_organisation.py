# coding=utf-8
import ast

from django.db.models.functions import Lower
from rest_framework.views import APIView

from base.models import Project
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import escape
from django.urls import reverse
from django.shortcuts import get_list_or_404
from django.db.models import Q, Prefetch
from django.http import HttpResponse, request
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView,
    TemplateView)
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.sessions.models import Session
from pure_pagination.mixins import PaginationMixin
from ..models import (
    CertifyingOrganisation,
    TrainingCenter,
    CourseType,
    CourseConvener,
    Course,
    CourseAttendee,
    CertifyingOrganisationCertificate,
    Checklist, OrganisationChecklist,
    REVIEWER, ORGANIZATION_OWNER, ExternalReviewer)
from ..forms import CertifyingOrganisationForm
from certification.utilities import check_slug
from ..serializers.checklist_serializer import ChecklistSerializer


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
        """Convert the context dictionary into a JSON object.

        :param context: Context data to use with template
        :type context: dict

        :return: JSON representation of the context
        :rtype: str
        """

        result = u'{\n'
        first_flag = True
        for certifyingorganisation in context['certifyingorganisations']:
            if not first_flag:
                result += u',\n'
            result += u'    "%s" : "%s"' % (
                certifyingorganisation.id, certifyingorganisation.name)
            first_flag = False
        result += u'\n}'
        return result


class CertifyingOrganisationMixin(object):
    """Mixin class to provide standard settings for Certifying Organisation."""

    model = CertifyingOrganisation
    form_class = CertifyingOrganisationForm


class CertifyingOrganisationUserTestMixin(UserPassesTestMixin, APIView):
    """Mixin class to provide update access to certifying organisation"""
    external_reviewer = None

    def test_func(self, user):
        certifying_organisation = (
            CertifyingOrganisation.objects.get(
                slug=self.kwargs.get('slug', None))
        )

        session = self.request.GET.get('s', None)

        if (
            user.is_staff or
            user in
            certifying_organisation.project.certification_managers.all() or
            user == certifying_organisation.project.owner
        ):
            return True

        if user.is_anonymous and session:
            try:
                session = Session.objects.get(
                    pk=session
                )
                self.external_reviewer = ExternalReviewer.objects.get(
                    session_key=session.pk,
                    certifying_organisation=certifying_organisation
                )
                return not self.external_reviewer.session_expired
            except (Session.DoesNotExist, ExternalReviewer.DoesNotExist):
                pass

        return False


class JSONCertifyingOrganisationListView(
    CertifyingOrganisationMixin, JSONResponseMixin, ListView):
    context_object_name = 'certifyingorganisation'

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
        return super(JSONCertifyingOrganisationListView, self).dispatch(
            request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Render this Certifying Organisation as markdown.

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """

        return self.render_to_json_response(context, **response_kwargs)


class CertifyingOrganisationListView(
    CertifyingOrganisationMixin,
    PaginationMixin,
    ListView):
    """List view for Certifying Organisation."""

    context_object_name = 'certifyingorganisations'
    template_name = 'certifying_organisation/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CertifyingOrganisationListView, self).get_context_data(**kwargs)
        context['num_certifyingorganisations'] = \
            context['certifyingorganisations'].count()
        context['unapproved'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
            context['project'] = context['the_project']
            context['certificate_lists'] = (
                CertifyingOrganisationCertificate.objects.filter(
                    certifying_organisation__project=context['the_project']
                ).values_list('certifying_organisation', flat=True)
            )
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
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                project = Project.objects.get(slug=project_slug)
                queryset = CertifyingOrganisation.objects.filter(
                    project=project, approved=True, enabled=True)
                return queryset
            else:
                raise Http404('Sorry! We could not find '
                              'your Certifying Organisation!')
        return self.queryset


class CertifyingOrganisationDetailView(
    CertifyingOrganisationMixin,
    DetailView):
    """Detail view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CertifyingOrganisationDetailView, self).get_context_data(**kwargs)

        certifying_organisation = self.object
        project_slug = self.kwargs.get('project_slug', None)

        # Check session key
        session_key = self.request.GET.get('s', None)
        session = None
        if session_key:
            try:
                session = Session.objects.get(pk=session_key)
            except Session.DoesNotExist:
                pass

        external_reviewers = ExternalReviewer.objects.filter(
            certifying_organisation=certifying_organisation
        ).order_by('id')
        context['external_reviewers'] = []
        for external_reviewer in external_reviewers:
            if not external_reviewer.session_expired:
                context['external_reviewers'].append(
                    external_reviewer
                )

        if certifying_organisation.approved:
            context['trainingcenters'] = TrainingCenter.objects.filter(
                certifying_organisation=certifying_organisation)
            context['num_trainingcenter'] = context['trainingcenters'].count()
            context['coursetypes'] = CourseType.objects.filter(
                certifying_organisation=certifying_organisation)
            context['num_coursetype'] = context['coursetypes'].count()
            context['courseconveners'] = CourseConvener.objects.filter(
                certifying_organisation=certifying_organisation
            ).prefetch_related('course_set')
            context['num_courseconvener'] = context['courseconveners'].count()
            context['courses'] = Course.objects.filter(
                certifying_organisation=certifying_organisation).order_by(
                '-start_date'
            )
            context['num_course'] = context['courses'].count()
            context['attendee'] = CourseAttendee.objects.filter(
                course__in=context['courses'],
                attendee__certifying_organisation=certifying_organisation
            )
            context['num_attendees'] = context['attendee'].count()

        context['project_slug'] = project_slug
        context['the_project'] = Project.objects.get(slug=project_slug)

        context['available_status'] = (
            context['the_project'].status_set.all().values_list(
                Lower('name'), flat=True
            )
        )
        context['project'] = context['the_project']

        user_can_create = False
        user_can_delete = False
        user_can_update_status = False
        user_can_invite_external_reviewer = False

        if (
            self.request.user.is_staff or
            self.request.user in context[
                'the_project'].certification_managers.all() or
            self.request.user == context['project'].owner
        ):
            user_can_create = True
            user_can_delete = True
            user_can_update_status = True
            user_can_invite_external_reviewer = True

        if self.request.user in \
                certifying_organisation.organisation_owners.all():
            if (
                certifying_organisation.approved or
                certifying_organisation.rejected or
                (
                    certifying_organisation.status and
                    certifying_organisation.status.name.lower() == 'pending'
                )
            ):
                user_can_create = True
                user_can_delete = True

        if session:
            try:
                external_reviewer = ExternalReviewer.objects.get(
                    session_key=session.session_key,
                    certifying_organisation=certifying_organisation
                )
                if not external_reviewer.session_expired:
                    user_can_update_status = True
            except ExternalReviewer.DoesNotExist:
                pass

        context['user_can_delete'] = user_can_delete
        context['user_can_create'] = user_can_create
        context['user_can_update_status'] = user_can_update_status
        context['user_can_invite_external_reviewer'] = (
            user_can_invite_external_reviewer
        )

        checklist_questions = Checklist.objects.filter(
            project=context['the_project'],
            target=REVIEWER,
            active=True
        ).prefetch_related(
            Prefetch(
                'organisationchecklist_set',
                queryset=OrganisationChecklist.objects.filter(
                    organisation=certifying_organisation
                ))
        )
        context['available_checklist'] = ChecklistSerializer(
            checklist_questions, many=True).data

        context['submitted_checklist'] = OrganisationChecklist.objects.filter(
            organisation=certifying_organisation,
        )

        context['checked_checklist'] = context['submitted_checklist'].filter(
            checklist__in=checklist_questions,
            checked=True
        ).count()

        # Get history data
        context['history'] = certifying_organisation.history.all()

        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is filtered to only show
                    approved Certifying Organisation.
        :rtype: QuerySet
        """

        qs = CertifyingOrganisation.objects.filter(rejected=False)
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Certifying Organisation slugs are unique within a Project,
        we need to make sure that we fetch the correct
        Certifying Organisation from the correct Project

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
                    raise Http404('Sorry! We could not find '
                                  'your Project!')
                try:
                    obj = queryset.get(project=project, slug=slug)
                except CertifyingOrganisation.DoesNotExist:
                    raise Http404('Sorry! We could not find '
                                  'your Certifying Organisation!')
                return obj
            else:
                raise Http404('Sorry! We could not find '
                              'your Certifying Organisation!')


class CertifyingOrganisationArchivingView(
    LoginRequiredMixin,
    CertifyingOrganisationMixin,
    APIView):
    """Archive/Unarchive Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/toogle_archive.html'

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """

        self.project_slug = kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        toogle_archive = kwargs.get('toogle_archive', 'unarchive')
        return render(
            request, self.template_name, {
                'toogle_archive': toogle_archive,
                'certifyingorganisation': CertifyingOrganisation.objects.get(
                    slug=kwargs.get('slug', None))
            })

    def post(self, request, *args, **kwargs):
        """Archive/Unarchive Certifying Organisation.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: HTTP response object
        :rtype: HttpResponse
        """

        certifying_organisation = CertifyingOrganisation.objects.get(
            slug=kwargs.get('slug', None))
        toogle_archive = kwargs.get('toogle_archive', 'unarchive')
        is_archived = str(toogle_archive).lower() == 'archive'
        certifying_organisation.is_archived = is_archived
        certifying_organisation.save()

        return HttpResponseRedirect(
            reverse('certifyingorganisation-list', kwargs={
                'project_slug': certifying_organisation.project.slug
            })
        )


# noinspection PyAttributeOutsideInit
class CertifyingOrganisationDeleteView(
    LoginRequiredMixin,
    CertifyingOrganisationMixin,
    DeleteView):
    """Delete view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project.

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
        return super(
            CertifyingOrganisationDeleteView, self) \
            .get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project.

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
        return super(
            CertifyingOrganisationDeleteView, self) \
            .post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation list page
        for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('certifyingorganisation-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the CertifyingOrganisation objects by
        Project before passing to get_object() to ensure that we
        return the correct Certifying Organisation object.
        The requesting User must be authenticated.

        :returns: Certifying Organisation queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated:
            raise Http404
        qs = CertifyingOrganisation.objects.filter(project=self.project)
        return qs


class CustomSuccessMessageMixin(object):
    """
    Adds a success message and extra tags on successful form submission.
    """
    success_message = ''
    message_extra_tags = ''

    def form_valid(self, form):
        response = super(CustomSuccessMessageMixin, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        message_extra_tags = self.get_extra_tags(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message, message_extra_tags)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_extra_tags(self, cleaned_data):
        return self.message_extra_tags % cleaned_data


# noinspection PyAttributeOutsideInit
class CertifyingOrganisationCreateView(
    CustomSuccessMessageMixin,
    LoginRequiredMixin,
    CertifyingOrganisationMixin,
    CreateView):
    """Create view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/create.html'
    success_message = 'Your organisation is successfully registered. ' \
                      'It is now waiting for an approval.'
    message_extra_tags = 'organisation_submitted'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the unapproved Certifying Organisation list page
        for the object's parent Project.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('pending-certifyingorganisation-list', kwargs={
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
            CertifyingOrganisationCreateView, self).get_context_data(**kwargs)
        context['certifyingorganisations'] = \
            self.get_queryset().filter(project=self.project)
        context['the_project'] = self.project
        context['available_checklist'] = ChecklistSerializer(
            Checklist.objects.filter(
                project=context['the_project'],
                target=ORGANIZATION_OWNER,
                active=True
            ), many=True).data
        return context

    def form_valid(self, form):
        """Save new created Certifying Organisation

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect

        We check that there is no referential integrity error when saving."""

        try:
            super(CertifyingOrganisationCreateView, self).form_valid(form)
            site = self.request.get_host()
            recipients = [self.project.owner, ]
            for manager in self.project.certification_managers.all():
                recipients.append(manager)

            for recipient in recipients:
                data = {
                    'recipient_firstname': recipient.first_name,
                    'recipient_lastname': recipient.last_name,
                    'project_name': self.project.name,
                    'site': site,
                    'project_slug': self.project_slug,
                    'org': self.object.slug,
                    'organisation_name': self.object.name,
                    'organisation_country': self.object.country.name,
                }

                # Send email notification to project owner and
                # certification managers
                send_mail(
                    u'Projecta - New Pending Organisation Approval',
                    u'Dear {recipient_firstname} {recipient_lastname},\n\n'
                    u'You have a new organisation registered to your '
                    u'project: {project_name}.\n'
                    u'Organisation name: {organisation_name}\n'
                    u'Country: {organisation_country}\n'
                    u'You may review and approve the organisation by '
                    u'following this link:\n'
                    u'{site}/en/{project_slug}/certifyingorganisation/{org}/'
                    u'\n\n'
                    u'Sincerely,\n\n\n\n\n'
                    u'------------------------------------------------------\n'
                    u'This is an auto-generated email from the system.'
                    u' Please do not reply to this email.'.format(**data),
                    self.project.owner.email,
                    [recipient.email],
                    fail_silently=False,
                )

            contact_person = \
                u'{} {}: {}\n'.format(
                    self.project.owner.first_name,
                    self.project.owner.last_name,
                    self.project.owner.email)

            for manager in self.project.certification_managers.all():
                contact_person += \
                    u'{} {}: {}\n'.format(
                        manager.first_name, manager.last_name, manager.email)

            # Email the applicant notify that the organisation is successfully
            # submitted.
            for applicant in self.object.organisation_owners.all():
                email_data = {
                    'applicant_firstname': applicant.first_name,
                    'applicant_lastname': applicant.last_name,
                    'contact_person': contact_person,
                }

                send_mail(
                    u'Projecta - Your Organisation is Successfully Submitted',
                    u'Dear {applicant_firstname} {applicant_lastname},\n\n'
                    u'Your organisation is successfully submitted.\n'
                    u'It is now waiting for an approval from the project\'s '
                    u'owner and certification managers.\n'
                    u'If you have not heard from us in few weeks you may '
                    u'contact us:\n'
                    u'{contact_person}'
                    u'\n\nSincerely,\n'.format(**email_data),
                    self.project.owner.email,
                    [applicant.email]
                )

            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                'ERROR: Certifying organisation by this name already exists!')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            CertifyingOrganisationCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs


# noinspection PyAttributeOutsideInit
class CertifyingOrganisationUpdateView(
    LoginRequiredMixin,
    CertifyingOrganisationMixin,
    UpdateView):
    """Update view for Certifying Organisation."""

    context_object_name = 'certifyingorganisation'
    template_name = 'certifying_organisation/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            CertifyingOrganisationUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        show_owner_message = False
        certifying_organisation = self.object
        if (
                certifying_organisation and
                self.request.user in
                certifying_organisation.organisation_owners.all()):
            show_owner_message = True
        kwargs.update({
            'user': self.request.user,
            'project': self.project,
            'form_title': 'Update Certifying Organisation',
            'show_owner_message': show_owner_message
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            CertifyingOrganisationUpdateView, self).get_context_data(**kwargs)
        context['certifyingorganisation'] = self.object
        context['certifyingorganisations'] = self.get_queryset() \
            .filter(project=self.project)
        context['the_project'] = self.project
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        projects which user created (staff gets all projects)
        :rtype: QuerySet
        """

        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        if self.request.user.is_staff:
            queryset = CertifyingOrganisation.objects.all()
        else:
            queryset = CertifyingOrganisation.objects.filter(
                Q(project=self.project) &
                (Q(project__owner=self.request.user) |
                 Q(organisation_owners=self.request.user) |
                 Q(project__certification_managers=self.request.user))
            ).distinct()
        return queryset

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the Certifying Organisation list page for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('certifyingorganisation-detail', kwargs={
            'slug': self.object.slug,
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""

        try:
            return super(
                CertifyingOrganisationUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Certifying Organisation by '
                'this name is already exists!')


class CertifyingOrganisationJson(BaseDatatableView):
    model = CertifyingOrganisation
    columns = ['name', 'creation_date', 'update_date',
               'org_name', 'can_approve', 'project_slug',
               'org_slug', 'country_name', 'can_edit',
               'status', 'remarks']
    order_columns = ['name']
    max_display_length = 100

    def get_initial_queryset(self):
        return CertifyingOrganisation.objects.all()

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'org_name':
            return escape('{0}'.format(row.name))
        elif column == 'status' or column == 'remarks':
            column_value = getattr(row, column)
            return escape('{0}'.format(column_value if column_value else ''))
        elif column == 'project_slug':
            return escape('{0}'.format(row.project.slug))
        elif column == 'org_slug':
            return escape('{0}'.format(row.slug))
        elif column == 'country_name':
            return escape('{0}'.format(row.country.name))
        elif column == 'creation_date':
            return escape('{0}'.format(row.creation_date))
        elif column == 'update_date':
            return escape('{0}'.format(row.update_date))
        elif column == 'can_approve':
            return (
                not row.approved and self.request.user.is_staff or
                self.request.user == row.project.owner or
                self.request.user in row.project.certification_managers.all()
            )
        elif column == 'can_edit':
            return (
                not row.approved and self.request.user.is_staff or
                self.request.user == row.project.owner or
                self.request.user == row.organisation_owners.all() or
                self.request.user in row.project.certification_managers.all()
            )
        else:
            return super(CertifyingOrganisationJson, self
                         ).render_column(row, column)

    def _validate_param(self, param_value):
        """
        Handle empty or invalid param value
        """
        try:
            param = ast.literal_eval(param_value)
            if not isinstance(param, bool):
                param = False
        except (ValueError, SyntaxError):
            param = False
        return param


    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        ready = self._validate_param(
            self.request.GET.get('ready', 'False'))
        approved = self._validate_param(
            self.request.GET.get('approved', 'False'))
        rejected = self._validate_param(
            self.request.GET.get('rejected', 'False'))
        is_archived = self._validate_param(
            self.request.GET.get('is_archived', 'False'))

        if not is_archived:
            qs = qs.filter(
                rejected=rejected,
                approved=approved,
                is_archived=is_archived
            )

            if approved:
                qs = qs.filter(enabled=True)
            else:
                if not ready:
                    qs = qs.filter(status__name__icontains='pending')
                else:
                    qs = qs.exclude(status__name__icontains='pending')
        else:
            qs = qs.filter(is_archived=is_archived)

        if search:
            qs = qs.filter(name__istartswith=search)
        return qs


class PendingCertifyingOrganisationListView(
    LoginRequiredMixin,
    CertifyingOrganisationMixin,
    PaginationMixin,
    ListView):
    """List view for pending certifying organisation."""

    context_object_name = 'certifyingorganisations'
    template_name = 'certifying_organisation/pending-list.html'
    paginate_by = 10

    def __init__(self):
        """
        We overload __init__ in order to declare self.project and
        self.project_slug. Both are then defined in self.get_queryset
        which is the first method called. This means we can then reuse the
        values in self.get_context_data.
        """

        super(PendingCertifyingOrganisationListView, self).__init__()
        self.project = None
        self.project_slug = None

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(PendingCertifyingOrganisationListView, self) \
            .get_context_data(**kwargs)
        context['num_certifyingorganisations'] = self.get_queryset().count()
        context['pending'] = (
            self.request.GET.get('ready', '').lower() == 'false'
        )
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
        return context

    # noinspection PyAttributeOutsideInit
    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show unapproved
        Certifying Organisation.
        :rtype: QuerySet
        :raises: Http404
        """

        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            if self.project_slug:
                self.project = Project.objects.get(slug=self.project_slug)
                if self.request.user.is_staff:
                    queryset = \
                        CertifyingOrganisation.unapproved_objects.filter(
                            project=self.project)
                else:
                    queryset = \
                        CertifyingOrganisation.unapproved_objects.filter(
                            Q(project=self.project) &
                            (Q(project__owner=self.request.user) |
                             Q(organisation_owners=self.request.user) |
                             Q(project__certification_managers=
                               self.request.user))).distinct()
                return queryset
            else:
                raise Http404(
                    'Sorry! We could not find your Certifying Organisation!')
        return self.queryset


def send_approved_email(
        certifying_organisation: CertifyingOrganisation,
        site: request):
    for organisation_owner in \
            certifying_organisation.organisation_owners.all():
        data = {
            'owner_firstname': organisation_owner.first_name,
            'owner_lastname': organisation_owner.last_name,
            'organisation_name': certifying_organisation.name,
            'project_name': certifying_organisation.project.name,
            'project_owner_firstname':
                certifying_organisation.project.owner.first_name,
            'project_owner_lastname':
                certifying_organisation.project.owner.last_name,
            'site': site,
            'project_slug': certifying_organisation.project.slug,
        }
        send_mail(
            u'Projecta - Your organisation is approved',
            u'Dear {owner_firstname} {owner_lastname},\n\n'
            u'Congratulations!\n'
            u'Your certifying organisation has been approved. The '
            u'following is the details of the newly approved organisation:'
            u'\n'
            u'Name of organisation: {organisation_name}\n'
            u'Project: {project_name}\n'
            u'You may now start creating your training center, '
            u'course type, course convener and course.\n'
            u'For further information please visit: '
            u'{site}/en/{project_slug}/about/\n\n'
            u'Sincerely,\n'
            u'{project_owner_firstname} {project_owner_lastname}'.format(
                **data),
            certifying_organisation.project.owner.email,
            [organisation_owner.email],
            fail_silently=False,
        )


class ApproveCertifyingOrganisationView(
    CertifyingOrganisationMixin,
    RedirectView):
    """Redirect view for approving Certifying Organisation."""

    permanent = False
    query_string = True
    pattern_name = 'certifyingorganisation-list'

    def get_redirect_url(self, project_slug, slug):
        """Save Certifying Organisation as approved and redirect.

        :param project_slug: The slug of the parent
                            Certifying Organisation's parent Project.
        :type project_slug: str

        :param slug: The slug of the Certifying Organisation.
        :type slug: str

        :returns: URL
        :rtype: str
        """

        certifyingorganisation_qs = \
            CertifyingOrganisation.unapproved_objects.all()
        # Get the object, when there is slug duplicate, get the first object
        certifyingorganisation = \
            get_list_or_404(certifyingorganisation_qs, slug=slug)[0]
        certifyingorganisation.approved = True

        # Check if slug have duplicates in approved objects.
        # If there is duplicate slug, assign new slug.
        approved_objects = CertifyingOrganisation.approved_objects.all()
        slug = check_slug(approved_objects, certifyingorganisation.slug)
        certifyingorganisation.slug = slug

        certifyingorganisation.save()

        site = self.request.get_host()

        send_approved_email(
            certifyingorganisation,
            site
        )

        return reverse(self.pattern_name, kwargs={
            'project_slug': project_slug
        })


class ArchivedCertifyingOrganisationListView(
    LoginRequiredMixin,
    CertifyingOrganisationMixin,
    PaginationMixin,
    ListView):
    """List view for archived certifying organisation."""

    context_object_name = 'certifyingorganisations'
    template_name = 'certifying_organisation/archived-list.html'
    paginate_by = 10

    def __init__(self):
        """
        We overload __init__ in order to declare self.project and
        self.project_slug. Both are then defined in self.get_queryset
        which is the first method called. This means we can then reuse the
        values in self.get_context_data.
        """

        super(ArchivedCertifyingOrganisationListView, self).__init__()
        self.project = None
        self.project_slug = None

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(ArchivedCertifyingOrganisationListView, self) \
            .get_context_data(**kwargs)
        context['num_certifyingorganisations'] = self.get_queryset().count()
        context['project_slug'] = self.project_slug
        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show archived
        Certifying Organisation.
        :rtype: QuerySet
        :raises: Http404
        """

        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            if self.project_slug:
                self.project = Project.objects.get(slug=self.project_slug)
                if self.request.user.is_staff:
                    queryset = \
                        CertifyingOrganisation.archived_objects.filter(
                            project=self.project)
                else:
                    queryset = \
                        CertifyingOrganisation.archived_objects.filter(
                            Q(project=self.project) &
                            (Q(project__owner=self.request.user) |
                             Q(organisation_owners=self.request.user) |
                             Q(project__certification_managers=
                               self.request.user))).distinct()
                return queryset
            else:
                raise Http404(
                    'Sorry! We could not find your Certifying Organisation!')
        return self.queryset


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(AboutView, self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug')
        context['the_project'] = Project.objects.get(slug=project_slug)
        return context


def send_rejection_email(certifying_organisation, site, schema='http'):
    """Send notification to owner that the organisation has been rejected"""
    for organisation_owner in \
            certifying_organisation.organisation_owners.all():
        data = {
            'owner_firstname': organisation_owner.first_name,
            'owner_lastname': organisation_owner.last_name,
            'organisation_name': certifying_organisation.name,
            'project_name': certifying_organisation.project.name,
            'project_owner_firstname':
                certifying_organisation.project.owner.first_name,
            'project_owner_lastname':
                certifying_organisation.project.owner.last_name,
            'site': site,
            'project_slug': certifying_organisation.project.slug,
            'status': certifying_organisation.status,
            'schema': schema
        }
        send_mail(
            u'Projecta - Your organisation is not approved',
            u'Dear {owner_firstname} {owner_lastname},\n\n'
            u'We are sorry that your certifying organisation '
            u'has not been approved. \nThe '
            u'following is the details of your organisation:'
            u'\n\n'
            u'Name of organisation: {organisation_name}\n'
            u'Project: {project_name}\n'
            u'Status: {status}\n\n'
            u'For further information please visit: '
            u'{schema}://{site}/en/{project_slug}/about/\n\n'
            u'Sincerely,\n'
            u'{project_owner_firstname} {project_owner_lastname}'.format(
                **data),
            certifying_organisation.project.owner.email,
            [organisation_owner.email],
            fail_silently=False,
        )


def reject_certifying_organisation(request, **kwargs):
    """Function to reject a pending certifying organisation."""

    pattern_name = 'pending-certifyingorganisation-list'

    if request.method == 'GET':
        project_slug = kwargs.pop('project_slug')
        slug = kwargs.pop('slug')

        certifyingorganisation_qs = \
            CertifyingOrganisation.objects.all()

        # Get the object, when there is slug duplicate, get the first object
        certifyingorganisation = \
            get_list_or_404(certifyingorganisation_qs, slug=slug)[0]
        certifyingorganisation.rejected = True
        certifyingorganisation.approved = False

        remarks = request.GET.get('remarks', '')
        certifyingorganisation.remarks = remarks

        # Check if slug have duplicates in rejected objects.
        # If there is duplicate slug, assign new slug.
        rejected_objects = CertifyingOrganisation.objects.filter(rejected=True)
        slug = check_slug(rejected_objects, certifyingorganisation.slug)
        certifyingorganisation.slug = slug

        certifyingorganisation.save()

        schema = request.is_secure() and "https" or "http"
        site = request.get_host()

        send_rejection_email(
            certifyingorganisation,
            site,
            schema
        )

        url = reverse(pattern_name, kwargs={
            'project_slug': project_slug
        })
        return HttpResponseRedirect(url)
    else:
        return HttpResponse('Please use GET method.')
