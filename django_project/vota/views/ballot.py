# coding=utf-8
"""Views for projects."""
# noinspection PyUnresolvedReferences
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404
import logging
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, \
    CreateView, DeleteView, UpdateView, ListView
from base.models import Project
from vota.forms import BallotCreateForm
from vota.models import Ballot, Committee

logger = logging.getLogger(__name__)


class BallotMixin(object):
    model = Ballot
    form_class = BallotCreateForm


class BallotDetailView(LoginRequiredMixin, BallotMixin, DetailView):
    context_object_name = 'ballot'
    template_name = 'ballot/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BallotDetailView, self).get_context_data(**kwargs)
        context['committee'] = Committee.objects.get(
            id=self.object.committee.id)
        return context

    def get_queryset(self):
        ballot_qs = Ballot.objects.all()
        return ballot_qs

    def get_object(self, queryset=None):
        """
        Get the object for this view.
        Because Ballot slugs are unique within a Committee, we need to make
        sure that we fetch the correct Ballot from the correct Committee
        """
        if queryset is None:
            queryset = self.get_queryset()
            slug = self.kwargs.get('slug', None)
            project_slug = self.kwargs.get('project_slug', None)
            committee_slug = self.kwargs.get('committee_slug', None)
            if slug and project_slug and committee_slug:
                project = Project.objects.get(slug=project_slug)
                committee = Committee.objects.filter(project=project)\
                    .get(slug=committee_slug)
                obj = queryset.get(slug=slug, committee=committee)
                return obj
            else:
                raise Http404

# noinspection PyAttributeOutsideInit
class BallotListView(BallotMixin, ListView):
    """Show all Ballots for a Committee

    This view returns a list of all Ballots within a Committee. The queryset
        returned is defined by the requesting user's status: is_authenticated
        and or is a member of the Committee

    """
    context_object_name = 'ballots'
    template_name = 'ballot/list.html'

    def get(self, request, *args, **kwargs):
        """Access URL parameters

        We need to define self.committee in order to return the correct set of
            Ballot objects

        :param request: Request object
        :type request: HttpRequestObject

        :param args: None

        :param kwargs: (django dict)
        :type kwargs: dict

        """
        committee_slug = self.kwargs.get('committee_slug')
        project_slug = self.kwargs.get('project_slug')
        try:
            self.project = Project.objects.get(slug=project_slug)
        except:
            raise Http404('Project could not be found')
        try:
            self.committee = Committee.objects.filter(
                project=self.project).get(slug=committee_slug)
        except:
            raise Http404('Committee could not be found')
        self.is_member = False
        if request.user in self.committee.users.all():
            self.is_member = True
        return super(BallotListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add to the context

        We need to add the Committee object to the context

        :param kwargs: (django dict)
        :type kwargs: dict

        """
        context = super(BallotListView, self).get_context_data(**kwargs)
        context['committee'] = self.committee
        context['is_member'] = self.is_member
        return context

    def get_queryset(self):
        """Specify the queryset

        Return a specific queryset based on the requesting user's status

        :return: If user.is_authenticated and a member of the Committee: All
            public Ballots, both open and closed.
            If not user.is_authenticated: All public ballots, both open and
            closed
        :rtype: QuerySet

        """
        if self.request.user.is_authenticated() and self.is_member:
                qs = Ballot.objects.filter(committee=self.committee)
        else:
            qs = Ballot.objects.filter(committee=self.committee) \
                .filter(private=False)
        return qs

# noinspection PyAttributeOutsideInit
class BallotCreateView(LoginRequiredMixin, BallotMixin, CreateView):
    context_object_name = 'ballot'
    template_name = 'ballot/create.html'

    def get_context_data(self, **kwargs):
        context = super(BallotCreateView, self).get_context_data(**kwargs)
        context['committee'] = self.committee
        return context

    def get_form_kwargs(self):
        kwargs = super(BallotCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.committee_slug = self.kwargs.get('committee_slug', None)
        self.committee = Committee.objects.filter(project=self.project)\
            .get(slug=self.committee_slug)
        kwargs.update({
            'user': self.request.user,
            'committee': self.committee
        })
        return kwargs

    def get_success_url(self):
        return reverse('ballot-detail', kwargs={
            'project_slug': self.object.committee.project.slug,
            'committee_slug': self.object.committee.slug,
            'slug': self.object.slug
        })

# noinspection PyAttributeOutsideInit
class BallotUpdateView(LoginRequiredMixin, BallotMixin, UpdateView):
    context_object_name = 'ballot'
    template_name = 'ballot/update.html'

    def get(self, request, *args, **kwargs):
        self.project_slug = kwargs.get('project_slug', None)
        self.committee_slug = kwargs.get('committee_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.committee = Committee.objects.filter(project=self.project)\
            .get(slug=self.committee_slug)
        return super(BallotUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.project_slug = kwargs.get('project_slug', None)
        self.committee_slug = kwargs.get('committee_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.committee = Committee.objects.filter(project=self.project)\
            .get(slug=self.committee_slug)
        return super(BallotUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        ballot_slug = self.kwargs.get('slug', None)
        filtered_queryset = queryset.filter(committee=self.committee)\
            .filter(committee__project=self.project)
        try:
            obj = filtered_queryset.get(slug=ballot_slug)
        except ObjectDoesNotExist:
            raise Http404('Sorry! We could not find your ballot!')
        except MultipleObjectsReturned:
            raise Http404('Sorry! For some reason, we found more than one '
                          'ballot!')
        return obj

    def get_context_data(self, **kwargs):
        context = super(BallotUpdateView, self).get_context_data(**kwargs)
        context['committee'] = self.committee
        return context

    def get_form_kwargs(self):
        kwargs = super(BallotUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.committee_slug = self.kwargs.get('committee_slug', None)
        self.committee = Committee.objects.filter(project=self.project)\
                .get(slug=self.committee_slug)
        kwargs.update({'user': self.request.user,'committee': self.committee
        })
        return kwargs

    def get_success_url(self):
        return reverse('ballot-detail', kwargs={
            'project_slug': self.object.committee.project.slug,
            'committee_slug': self.object.committee.slug,
            'slug': self.object.slug
        })

# noinspection PyAttributeOutsideInit
class BallotDeleteView(StaffuserRequiredMixin, BallotMixin, DeleteView):
    """The view for deleting a Ballot object.

    Accepts GET requests, returning a confirmation page and POST requests to
        confirm and trigger Ballot deletion.

    """
    context_object_name = 'ballot'
    template_name = 'ballot/delete.html'

    def get(self, request, *args, **kwargs):
        """Access URL parameters

        We need to define the Ballot object's parent Committee and Project in
            order to ensure that we return the correct Ballot.

        :param request: Request object
        :type request: dict

        :param args: None
        :type args: dict

        :param kwargs: (django dict)
        :type kwargs: dict

        :return: Super class
        :rtype: Request object

        """
        self.project_slug = kwargs.get('project_slug', None)
        self.committee_slug = kwargs.get('committee_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.committee = Committee.objects.filter(project=self.project) \
            .get(slug=self.committee_slug)
        return super(BallotDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Access URL parameters

        We need to define the Ballot object's parent Committee and Project in
            order to ensure that we return the correct Ballot.

        :param request: Request object
        :type request: dict

        :param args: None
        :type args: dict

        :param kwargs: (django dict)
        :type kwargs: dict

        :return: Super class
        :rtype: Request object

        """
        self.project_slug = kwargs.get('project_slug', None)
        self.committee_slug = kwargs.get('committee_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        self.committee = Committee.objects.filter(project=self.project) \
            .get(slug=self.committee_slug)
        return super(BallotDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        The user will be redirected to the detail view for the deleted Ballot
            object's parent Committee

        :return: Reversed URL
        :rtype: HttpResponse

        """
        return reverse('committee-detail', kwargs={
            'project_slug': self.project_slug,
            'slug': self.committee_slug
        })

    def get_queryset(self):
        """Define the queryset

        We override this method in order to make sure that the Ballot object
            returned is from the correct Committee. The requesting User must
            also be staff, so we confirm that here.

        :return: Ballot queryset
        :rtype: Queryset

        :raise Http404: If user is not staff

        """
        if not self.request.user.is_staff:
            raise Http404()
        return Ballot.objects.filter(committee=self.committee)
