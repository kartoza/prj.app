__author__ = 'rischan'


import os
import time
import logging

from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView)
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core import serializers
from django.template.loader import get_template

from braces.views import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from PIL import Image
from pinax.notifications.models import send

from base.models import Project
from ..models import Sponsor, SponsorshipPeriod, active_sustaining_membership  # noqa
from ..models import SponsorshipLevel  # noqa
from ..forms import SponsorForm

from ..utils import render_to_pdf
from changes import (
    NOTICE_SUSTAINING_MEMBER_APPROVED,
    NOTICE_SUSTAINING_MEMBER_REJECTED
)

logger = logging.getLogger(__name__)


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
        """Convert the context dictionary into a JSON object

        :param context: Context data to use with template
        :type context: dict

        :return: JSON representation of the context
        :rtype: str
        """
        result = '{\n'
        first_flag = True
        for sponsor in context['sponsors']:
            if not first_flag:
                result += ',\n'
            result += '    "%s" : "%s"' % (sponsor.id, sponsor.name)
            first_flag = False
        result += '\n}'
        return result


class SponsorMixin(object):
    """Mixin class to provide standard settings for Sponsor."""
    model = Sponsor  # implies -> queryset = Sponsor.objects.all()
    form_class = SponsorForm
    request = None

    def user_can_edit(self, sustaining_member, project):
        if not self.request:
            return False
        if (
                self.request.user.is_staff or
                self.request.user.is_superuser or
                self.request.user == sustaining_member.author or
                self.request.user in project.sponsorship_managers.all()):
            return True
        return False


class JSONSponsorListView(SponsorMixin, JSONResponseMixin, ListView):
    """List view for Sponsor as json object - needed by javascript."""
    context_object_name = 'sponsors'

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
        return super(JSONSponsorListView, self).dispatch(
            request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """Render this Sponsor as markdown.

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """
        return self.render_to_json_response(context, **response_kwargs)


class SponsorListView(SponsorMixin, PaginationMixin, ListView):
    """List view for Sponsor."""
    context_object_name = 'sponsors'
    template_name = 'sponsor/list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(SponsorListView, self).get_context_data(**kwargs)
        context['num_sponsors'] = context['sponsors'].count()
        context['unapproved'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            project = Project.objects.get(slug=project_slug)
            context['project'] = Project.objects.get(slug=project_slug)
            context['levels'] = SponsorshipLevel.objects.filter(
                project=project)
            context['is_sustaining_member'] = active_sustaining_membership(
                self.request.user,
                project
            ).exists()
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Sponsor Queryset which is filtered by project
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                project = Project.objects.get(slug=project_slug)
                queryset = SponsorshipPeriod.approved_objects.filter(
                    project=project,
                    sponsor__active=True
                ).order_by('-sponsorship_level__value')
                return queryset
            else:
                raise Http404('Sorry! We could not find your Sponsor!')
        return self.queryset


class FutureSponsorListView(
    LoginRequiredMixin, SponsorMixin, PaginationMixin, ListView):
    """List view for Sponsor."""
    context_object_name = 'sponsors'
    template_name = 'sponsor/future-list.html'
    paginate_by = 1000

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(FutureSponsorListView, self).get_context_data(**kwargs)
        context['num_sponsors'] = context['sponsors'].count()
        context['unapproved'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            project = Project.objects.get(slug=project_slug)
            # Checking user permissions.
            if self.request.user.is_staff or \
                    self.request.user == project.owner or \
                    self.request.user in project.sponsorship_managers.all()\
                    or self.request.user == project.project_representative:
                pass
            else:
                raise Http404

            context['project'] = Project.objects.get(slug=project_slug)
            context['levels'] = SponsorshipLevel.objects.filter(
                project=project)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Sponsor Queryset which is filtered by project
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                project = Project.objects.get(slug=project_slug)
                queryset = SponsorshipPeriod.approved_objects.filter(
                    project=project).order_by('-sponsorship_level__value')
                return queryset
            else:
                raise Http404('Sorry! We could not find your Sponsor!')
        return self.queryset


class SponsorWorldMapView(SponsorMixin, ListView):
    """World map view for Sponsors."""
    context_object_name = 'sponsors'
    template_name = 'sponsor/world-map.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        project_slug = self.kwargs.get('project_slug', None)
        context = super(SponsorWorldMapView, self).get_context_data(**kwargs)
        if project_slug:
            context['project'] = Project.objects.get(slug=project_slug)
            project = Project.objects.get(slug=project_slug)
            levels = SponsorshipLevel.objects.filter(project=project)
            context['levels'] = serializers.serialize(
                "json",
                levels
            )
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Sponsor Queryset which is filtered by project
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            if project_slug:
                project = Project.objects.get(slug=project_slug)
                queryset = SponsorshipPeriod.objects.filter(project=project)
                return queryset
            else:
                raise Http404('Sorry! We could not find your Sponsor!')
        return self.queryset


class SponsorDetailView(SponsorMixin, DetailView):
    """Detail view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SponsorDetailView, self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        slug = self.kwargs.get('slug', None)
        context['project_slug'] = project_slug
        context['slug'] = self.kwargs.get('slug', None)
        if project_slug:
            context['project'] = Project.objects.get(slug=project_slug)
            sustaining_member = self.get_object()
            context['user_can_edit'] = self.user_can_edit(
                sustaining_member, context['project'])
            try:
                context['period'] = SponsorshipPeriod.objects.get(
                    Q(slug=slug) | Q(sponsor__slug=slug),
                    sponsor=sustaining_member,
                    project=context['project']
                )
            except SponsorshipPeriod.DoesNotExist:
                pass
        return context

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Sponsor slugs are unique within a Project, we need to make
        sure that we fetch the correct Sponsor from the correct Project

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a project
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            if slug and project_slug:
                project = Project.objects.get(slug=project_slug)
                try:
                    obj = Sponsor.objects.get(
                        Q(sponsorshipperiod__slug=slug) | Q(slug=slug),
                        project=project)
                    return obj
                except Sponsor.DoesNotExist:
                    return Http404('Sorry! we could not find your sponsor.')
            else:
                raise Http404('Sorry! We could not find your sponsor!')


# noinspection PyAttributeOutsideInit
class SponsorDeleteView(LoginRequiredMixin, SponsorMixin, DeleteView):
    """Delete view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the project_slug from the URL and define the Project

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
        return super(SponsorDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project

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
        return super(SponsorDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion  of the object, the User will be redirected
        to the Sponsor list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('sponsor-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the Sponsor objects by Project before passing to
        get_object() to ensure that we return the correct Sponsor object.
        The requesting User must be authenticated

        :returns: Sponsor queryset filtered by Project
        :rtype: QuerySet
        :raises: Http404
        """
        if not self.request.user.is_authenticated:
            raise Http404
        qs = Sponsor.objects.filter(project=self.project)
        return qs


# noinspection PyAttributeOutsideInit
class SponsorCreateView(LoginRequiredMixin, SponsorMixin, CreateView):
    """Create view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/create.html'

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Sponsor list page for the object's parent Project

       :returns: URL
       :rtype: HttpResponse
       """
        return reverse('pending-sponsor-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SponsorCreateView, self).get_context_data(**kwargs)
        context['sponsors'] = self.get_queryset() \
            .filter(project=self.project)
        context['project'] = self.project
        return context

    def form_valid(self, form):
        """Save new created Sponsor

        :param form
        :type form

        :returns HttpResponseRedirect object to success_url
        :rtype: HttpResponseRedirect

        We check that there is no referential integrity error when saving."""
        try:
            super(SponsorCreateView, self).form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            return ValidationError(
                'ERROR: Sponsor by this name already exists!')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SponsorCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs


# noinspection PyAttributeOutsideInit
class SponsorUpdateView(LoginRequiredMixin, SponsorMixin, UpdateView):
    """Update view for Sponsor."""
    context_object_name = 'sponsor'
    template_name = 'sponsor/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(SponsorUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(SponsorUpdateView, self).get_context_data(**kwargs)
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
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            if slug and project_slug:
                project = Project.objects.get(slug=project_slug)
                try:
                    obj = Sponsor.objects.get(
                        Q(sponsorshipperiod__slug=slug) | Q(slug=slug),
                        project=project)
                    return obj
                except Sponsor.DoesNotExist:
                    return None
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
        return reverse('sponsor-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(SponsorUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Sponsor by this name already exists!')


class PendingSponsorListView(
    LoginRequiredMixin, SponsorMixin, PaginationMixin, ListView):  # noqa
    """List view for pending Sponsor."""
    context_object_name = 'sponsors'
    template_name = 'sponsor/pending-list.html'
    paginate_by = 10

    def __init__(self):
        """
        We overload __init__ in order to declare self.project and
        self.project_slug. Both are then defined in self.get_queryset
        which is the first method called. This means we can then reuse the
        values in self.get_context_data.
        """
        super(PendingSponsorListView, self).__init__()
        self.project = None
        self.project_slug = None

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(PendingSponsorListView, self)\
            .get_context_data(**kwargs)
        context['num_sponsors'] = self.get_queryset().count()
        context['unapproved'] = True
        context['project_slug'] = self.project_slug
        context['project'] = self.project
        return context

    # noinspection PyAttributeOutsideInit
    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show unapproved
        Sponsor.
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            if self.project_slug:
                self.project = Project.objects.get(slug=self.project_slug)
                queryset = Sponsor.pending_objects.filter(
                    project=self.project)
                return queryset
            else:
                raise Http404('Sorry! We could not find your sponsor!')
        return self.queryset


class ApproveSponsorView(LoginRequiredMixin, SponsorMixin, RedirectView):
    """Redirect view for approving Sponsor."""
    permanent = False
    query_string = True
    pattern_name = 'pending-sponsor-list'

    def get_redirect_url(self, project_slug, slug):
        """Save Sponsor as approved and redirect

        :param project_slug: The slug of the parent Sponsor's parent Project
        :type project_slug: str

        :param slug: The slug of the Sponsor
        :type slug: str

        :returns: URL
        :rtype: str
        """
        if self.request.user.is_staff:
            sponsor_qs = Sponsor.unapproved_objects.all()
        else:
            sponsor_qs = Sponsor.unapproved_objects.filter(
                Q(project__owner=self.request.user) |
                Q(project__sponsorship_managers=self.request.user))
        sponsor = get_object_or_404(sponsor_qs, slug=slug)
        sponsor.approved = True
        sponsor.rejected = False
        sponsor.remarks = ''
        project = Project.objects.get(
            slug=self.kwargs.get('project_slug')
        )
        sponsorship_managers = project.sponsorship_managers.all()
        send([
                 self.request.user,
             ] + list(sponsorship_managers),
             NOTICE_SUSTAINING_MEMBER_APPROVED,
             {'sustaining_member_name': sponsor.name})
        sponsor.save()
        return reverse(self.pattern_name, kwargs={
            'project_slug': project_slug
        })


class RejectSponsorView(LoginRequiredMixin, SponsorMixin, RedirectView):
    """Redirect view for rejecting Sponsor."""
    permanent = False
    query_string = True
    pattern_name = 'pending-sponsor-list'

    def get_redirect_url(self, project_slug, member_id):
        """Save Sponsor as Rejected and redirect

        :param project_slug: The slug of the parent Sponsor's parent Project
        :type project_slug: str

        :param member_id: The id of the Sponsor
        :type member_id: int

        :returns: URL
        :rtype: str
        """
        if self.request.user.is_staff:
            sponsor_qs = Sponsor.unapproved_objects.all()
        else:
            sponsor_qs = Sponsor.unapproved_objects.filter(
                Q(project__owner=self.request.user) |
                Q(project__sponsorship_managers=self.request.user))
        sponsor = get_object_or_404(sponsor_qs, id=member_id)
        sponsor.approved = False
        sponsor.rejected = True
        remarks = self.request.GET.get('remark', '')
        sponsor.remarks = remarks
        sponsor.save()
        project = Project.objects.get(
            slug=self.kwargs.get('project_slug')
        )
        sponsorship_managers = project.sponsorship_managers.all()
        send([
                 self.request.user,
             ] + list(sponsorship_managers),
             NOTICE_SUSTAINING_MEMBER_REJECTED,
             {'remarks': remarks, 'sustaining_member_name': sponsor.name})
        return reverse(self.pattern_name, kwargs={
            'project_slug': project_slug
        })


def generate_sponsor_cloud(request, **kwargs):
    """Generate image for sponsor logos."""

    project_slug = kwargs.pop('project_slug')
    project = Project.objects.get(slug=project_slug)
    project_name = project.name.lower().replace(' ', '_')
    queryset = SponsorshipPeriod.objects.filter(
        project=project).order_by('-sponsorship_level__value')
    background = Image.new("RGB", (1200, 1000), "white")
    max_x = 0
    max_y = 0
    y = 0
    x = 0
    sponsor_level = ''
    xy_size = 100
    for sponsor in queryset:
        if sponsor.current_sponsor():
            if sponsor.sponsorship_level.name != sponsor_level:
                if sponsor_level != '':
                    sponsor_level = sponsor.sponsorship_level.name
                    xy_size -= 25
                    y += 25
                    if xy_size < 25:
                        xy_size = 25
                        y -= 25
                else:
                    sponsor_level = sponsor.sponsorship_level.name

            im = Image.open(
                sponsor.sponsor.logo).convert("RGBA")
            size = xy_size, xy_size
            im.thumbnail(size, Image.ANTIALIAS)
            width, height = im.size
            if (x + xy_size) >= 1000:
                x = 0
                y += xy_size
            if max_x <= (x + xy_size):
                max_x = x + xy_size
            if max_y <= y:
                max_y = y + xy_size
            background.paste(
                im, box=(x, y + int((xy_size - height) / 2)), mask=im)
            x += xy_size

    image_path = 'none'
    if max_x != 0:
        filepath = '/home/web/media/images/sponsors/'
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        background.crop(
            (0, 0, max_x, max_y)).save(
            filepath + '{}.png'.format(project_name))

        image_path = \
            settings.MEDIA_URL + 'images/sponsors/{}.png'.format(project_name)

    return render(
        request, 'sponsor/sponsor_cloud.html',
        context={
            'image': image_path,
            'the_project': project})


class GenerateSponsorPDFView(LoginRequiredMixin, SponsorMixin, TemplateView):
    """Template View for invoice generation."""
    context_object_name = 'sponsors'
    template_name = 'sponsor/invoice.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(GenerateSponsorPDFView, self).\
            get_context_data(pagesize="A4", **kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        sponsor_slug = self.kwargs.get('slug', None)
        sponsors = SponsorshipPeriod.approved_objects.all()

        context['project_slug'] = project_slug
        context['sponsor_slug'] = sponsor_slug
        context['sponsors'] = sponsors
        context['date'] = time.strftime("%d/%m/%Y")
        if project_slug and sponsor_slug:
            project = Project.objects.get(slug=project_slug)
            context['sponsor'] = sponsors.get(
                project=project,
                slug=sponsor_slug)
            context['project'] = project
            context['title'] = '{}-{}'.format(
                project_slug,
                sponsor_slug,)
        return context

    def get(self, request, *args, **kwargs):
        template = get_template('sponsor/invoice.html')
        context = self.get_context_data(**kwargs)

        template.render(context)
        pdf = render_to_pdf('sponsor/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % (context['title'])
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class RejectedSustainingMemberList(
    LoginRequiredMixin, SponsorMixin, PaginationMixin, ListView):  # noqa
    """List view for pending Sustaining Members."""
    context_object_name = 'sustaining_members'
    template_name = 'sponsor/rejected-list.html'
    paginate_by = 10

    def __init__(self):
        """
        We overload __init__ in order to declare self.project and
        self.project_slug. Both are then defined in self.get_queryset
        which is the first method called. This means we can then reuse the
        values in self.get_context_data.
        """
        super(RejectedSustainingMemberList, self).__init__()
        self.project = None
        self.project_slug = None

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(RejectedSustainingMemberList, self)\
            .get_context_data(**kwargs)
        context['num_sponsors'] = self.get_queryset().count()
        context['rejected'] = True
        context['project_slug'] = self.project_slug
        context['project'] = self.project
        return context

    # noinspection PyAttributeOutsideInit
    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show unapproved
        Sponsor.
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            if self.project_slug:
                self.project = Project.objects.get(slug=self.project_slug)
                queryset = Sponsor.objects.filter(
                    rejected=True,
                    project=self.project)
                return queryset
            else:
                raise Http404('Sorry! We could not find your sponsor!')
        return self.queryset
