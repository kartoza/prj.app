# -*- coding: utf-8 -*-
"""**View classes for Version**

"""

# noinspection PyUnresolvedReferences
# import logging
from base.models import Project
# LOGGER = logging.getLogger(__name__)
import re
import zipfile
import StringIO
import pypandoc
from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView)
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from pure_pagination.mixins import PaginationMixin
from ..models import Version
from ..forms import VersionForm

__author__ = 'Tim Sutton <tim@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = ''
__license__ = ''
__copyright__ = ''


class VersionMixin(object):
    """Mixing for all views to inherit which sets some standard properties."""
    model = Version  # implies -> queryset = Version.objects.all()
    form_class = VersionForm


class VersionListView(VersionMixin, PaginationMixin, ListView):
    """List view for Version."""
    context_object_name = 'versions'
    template_name = 'version/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(VersionListView, self).get_context_data(**kwargs)
        context['num_versions'] = self.get_queryset().count()
        context['unapproved'] = False
        context['rst_download'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Version
        for this project.
        :rtype: QuerySet

        :raises: Http404
        """
        if self.request.user.is_staff:
            versions_qs = Version.objects.all()
        else:
            versions_qs = Version.approved_objects.all()

        project_slug = self.kwargs.get('project_slug', None)
        if project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
            except Project.DoesNotExist:
                raise Http404(
                    'The requested project does not exist.'
                )
            versions_qs = versions_qs.filter(
                project=project).order_by('-padded_version')
            return versions_qs
        else:
            raise Http404('Sorry! We could not find your version!')
        # In case no project filter applied
        return versions_qs


class VersionDetailView(VersionMixin, DetailView):
    """A tabular list style view for a Version."""
    context_object_name = 'version'
    template_name = 'version/detail.html'

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Versions.
        :rtype: QuerySet
        """
        if self.request.user.is_staff:
            versions_qs = Version.objects.all()
        else:
            versions_qs = Version.approved_objects.all()
        return versions_qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Version slugs are unique within a Project, we need to make
        sure that we fetch the correct Version from the correct Project

        :param queryset
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a project
        :rtype QuerySet
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
                raise Http404(
                    'Requested project does not exist.')
            try:
                obj = queryset.filter(project=project).get(slug=slug)
                return obj
            except Version.DoesNotExist:
                raise Http404(
                    'Sorry! The project you are requesting a version for '
                    'could not be found or you do not have permission to '
                    'view the version. Also the version may not be '
                    'approved yet. Try logging in as a staff member if '
                    'you wish to view it.')
        else:
            raise Http404('Sorry! We could not find your version!')


class VersionMarkdownView(VersionDetailView):
    """Return a markdown Version detail."""
    template_name = 'version/detail.md'

    def render_to_response(self, context, **response_kwargs):
        """Render this Version as markdown.

        :param context: Context data to use with template.
        :type context: dict

        :param response_kwargs: A dict of arguments to pass to the renderer.
        :type response_kwargs: dict

        :returns: A rendered template with mime type application/text.
        :rtype: HttpResponse
        """
        response = super(VersionMarkdownView, self).render_to_response(
            context,
            content_type='application/text',
            **response_kwargs)
        response['Content-Disposition'] = 'attachment; filename="foo.md"'
        return response


class VersionThumbnailView(VersionMixin, DetailView):
    """A contact sheet style list of thumbs per entry."""
    context_object_name = 'version'
    template_name = 'version/detail-thumbs.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(VersionThumbnailView, self).get_context_data(**kwargs)
        context['as_thumbs'] = True
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Versions.
        :rtype: QuerySet
        """
        if self.request.user.is_staff:
            versions_qs = Version.objects.all()
        else:
            versions_qs = Version.approved_objects.all()
        return versions_qs

    def get_object(self, queryset=None):
        """Get the object referenced by this view.

        :param queryset: An option queryset from which the object should be
            retrieved.
        :type queryset: QuerySet

        :returns: A Version instance.
        :rtype: Version
        """
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs.get('slug', None)
        project_slug = self.kwargs.get('project_slug', None)
        if slug and project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
            except Project.DoesNotExist:
                raise Http404(
                    'Sorry! The project you are requesting a version for '
                    'could not be found or you do not have permission to '
                    'view the version. Also the version may not be '
                    'approved yet. Try logging in as a staff member if '
                    'you wish to view it.')
            try:
                obj = queryset.filter(project=project).get(slug=slug)
                return obj
            except Version.DoesNotExist:
                raise Http404(
                    'Sorry! The version you are requesting '
                    'could not be found or you do not have permission to '
                    'view the version. Also the version may not be '
                    'approved yet. Try logging in as a staff member if '
                    'you wish to view it.')
        else:
            raise Http404('Sorry! We could not find your version!')


# noinspection PyAttributeOutsideInit
class VersionDeleteView(LoginRequiredMixin, VersionMixin, DeleteView):
    """Delete view for Entry."""
    context_object_name = 'version'
    template_name = 'version/delete.html'

    def get(self, request, *args, **kwargs):
        """Access URL parameters

        We need to make sure that we return the correct Version for the current
            project as defined in the URL

        :param request: The incoming HTTP request object
        :type request: Request object

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse

        """
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(VersionDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Access URL parameters

        We need to make sure that we return the correct Version for the current
        project as defined in the URL

        :param request: The incoming HTTP request object
        :type request: Request object

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        return super(VersionDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Define the redirect URL

        After successful deletion of the object, the User will be redirected
        to the Version list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('version-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which shows all Versions if user.is_staff,
                or only the creator's Versions if not user.is_staff.
        :rtype: QuerySet
        :raises: Http404
        """
        if not self.request.user.is_authenticated():
            raise Http404
        qs = Version.objects.filter(project=self.project)
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(author=self.request.user)


# noinspection PyAttributeOutsideInit
class VersionCreateView(LoginRequiredMixin, VersionMixin, CreateView):
    """Create view for Version."""
    context_object_name = 'version'
    template_name = 'version/create.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(VersionCreateView, self).get_context_data(**kwargs)
        context['versions'] = Version.objects.filter(project=self.project)
        return context

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Version list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('pending-version-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(VersionCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            result = super(VersionCreateView, self).form_valid(form)
            return result
        except IntegrityError:
            raise ValidationError(
                'ERROR: Version by this name already exists!')


# noinspection PyAttributeOutsideInit
class VersionUpdateView(StaffuserRequiredMixin, VersionMixin, UpdateView):
    """Update view for Version."""
    context_object_name = 'version'
    template_name = 'version/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(VersionUpdateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Versions.
        :rtype: QuerySet
        """
        if self.request.user.is_staff:
            versions_qs = Version.objects.all()
        else:
            versions_qs = Version.approved_objects.all()
        return versions_qs

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
            to the Version list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('version-list', kwargs={
            'project_slug': self.object.project.slug
        })

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            return super(VersionUpdateView, self).form_valid(form)
        except IntegrityError:
            raise ValidationError(
                'ERROR: Version by this name already exists!')


class PendingVersionListView(
        StaffuserRequiredMixin,
        VersionMixin,
        PaginationMixin,
        ListView):
    """List view for pending Version. Staff see all """
    context_object_name = 'versions'
    template_name = 'version/list.html'
    paginate_by = 10

    def __init__(self):
        """
        We overload __init__ in order to declare self.project and
        self.project_slug. Both are then defined in self.get_queryset which is
        the first method called. This means we can then reuse the values in
        self.get_context_data.
        """
        super(PendingVersionListView, self).__init__()
        self.project_slug = None
        self.project = None

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(PendingVersionListView, self).get_context_data(
            **kwargs)
        context['num_versions'] = self.get_queryset().count()
        context['unapproved'] = True
        context['project'] = self.project
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Version.
        :rtype: QuerySet
        :raises: Http404
        """
        if self.queryset is None:
            self.project_slug = self.kwargs.get('project_slug', None)
            if self.project_slug:
                self.project = Project.objects.get(slug=self.project_slug)
                queryset = Version.unapproved_objects.filter(
                    project=self.project)
                if self.request.user.is_staff:
                    return queryset
                else:
                    return queryset.filter(author=self.request.user)
            else:
                raise Http404('Sorry! We could not find your version!')
        return self.queryset


class ApproveVersionView(StaffuserRequiredMixin, VersionMixin, RedirectView):
    """View for approving Version."""
    permanent = False
    query_string = True
    pattern_name = 'version-list'

    def get_redirect_url(self, project_slug, slug):
        """Get the url for when the operation completes.

        :param project_slug: The slug of the Version's parent Project
        :type project_slug: str

        :param slug: The slug of the object being approved.
        :type slug: str

        :returns: A url.
        :rtype: str
        """
        project = Project.objects.get(slug=project_slug)
        version_qs = Version.unapproved_objects.filter(project=project)
        version = get_object_or_404(version_qs, slug=slug)
        version.approved = True
        version.save()
        return reverse(self.pattern_name, kwargs={
            'project_slug': version.project.slug
        })


class VersionDownload(VersionMixin, StaffuserRequiredMixin, DetailView):
    """View to allow staff users to download Version page in RST format"""
    template_name = 'version/detail-content.html'

    def render_to_response(self, context, **response_kwargs):
        """Returns a RST document for a project Version page.

        :param context:
        :type context: dict

        :param response_kwargs: Keyword Arguments
        :param response_kwargs: dict

        :returns: a RST document for a project Version page.
        :rtype: HttpResponse
        """
        version_obj = context.get('version')
        # set the context flag for 'rst_download'
        context['rst_download'] = True
        # render the template
        document = self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )
        # convert the html to rst
        converted_doc = pypandoc.convert(
            document.rendered_content.encode(
                'utf8', 'ignore'), 'rst', format='html')
        converted_doc = converted_doc.replace('/media/images/', 'images/')

        # prepare the ZIP file
        zip_file = self._prepare_zip_archive(converted_doc, version_obj)

        # Grab the ZIP file from memory, make response with correct MIME-type
        response = HttpResponse(
            zip_file.getvalue(), content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        response['Content-Disposition'] = (
            'attachment; filename="{}-{}.zip"'.format(
                version_obj.project.name, version_obj.name)
        )

        return response

    # noinspection PyMethodMayBeStatic
    def _prepare_zip_archive(self, document, version_obj):
        """Prepare a ZIP file with the document and referenced images.
        :param document:
        :param version_obj: Instance of a version object.

        :returns temporary path for the created zip file
        :rtype: string
        """
        # create in memory file-like object
        temp_path = StringIO.StringIO()

        # grab all of the images from document
        images = []
        for line in document.split('\n'):
            if 'image::' in line:
                matches = re.findall(r'images.+', line)
                images.extend(matches)

        # create the ZIP file
        with zipfile.ZipFile(temp_path, 'w') as zip_file:
            # write all of the image files (read from disk)
            for image in images:
                zip_file.write(
                    '../media/{0}'.format(image),
                    '{0}'.format(image)
                )
            # write the actual RST document
            zip_file.writestr(
                'index.rst',
                document)

        return temp_path


class VersionDownloadGnu(VersionMixin, DetailView):
    """A tabular list style view for a Version."""
    context_object_name = 'version'
    template_name = 'version/detail-titles.txt'

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved Versions.
        :rtype: QuerySet
        """
        if self.request.user.is_staff:
            versions_qs = Version.objects.all()
        else:
            versions_qs = Version.approved_objects.all()
        return versions_qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        Because Version slugs are unique within a Project, we need to make
        sure that we fetch the correct Version from the correct Project

        :param queryset
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a project
        :rtype QuerySet
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
                raise Http404(
                    'Requested project does not exist.')
            try:
                obj = queryset.filter(project=project).get(slug=slug)
                return obj
            except Version.DoesNotExist:
                raise Http404(
                    'Sorry! The project you are requesting a version for '
                    'could not be found or you do not have permission to '
                    'view the version. Also the version may not be '
                    'approved yet. Try logging in as a staff member if '
                    'you wish to view it.')
        else:
            raise Http404('Sorry! We could not find your version!')

    def get(self, request, *args, **kwargs):
        """We overload this so we can return a text document instead of html.

        :param request: An HttpRequest object.
        """
        self.object = self.get_object()
        context = self.get_context_data()

        return self.render_to_response(
            context,
            content_type="text/plain; charset=utf-8")


class VersionSponsorDownload(VersionMixin, StaffuserRequiredMixin, DetailView):
    """View to allow staff users to download Version page in html format"""
    template_name = 'version/includes/version-sponsors.html'

    def render_to_response(self, context, **response_kwargs):
        """Returns a html document for a project Version page.

        :param context:
        :type context: dict

        :param response_kwargs: Keyword Arguments
        :param response_kwargs: dict

        :returns: a html document for a project Version page.
        :rtype: HttpResponse
        """
        version_obj = context.get('version')
        # set the context flag for 'html_download'
        context['html_download'] = True
        # render the template
        document = self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )
        # convert the html to html
        converted_doc = pypandoc.convert(
            document.rendered_content.encode(
                'utf8', 'ignore'), 'html', format='html')
        converted_doc = converted_doc.replace('/media/images/', 'images/')

        # prepare the ZIP file
        zip_file = self._prepare_zip_archive(converted_doc, version_obj)

        # Grab the ZIP file from memory, make response with correct MIME-type
        response = HttpResponse(
            zip_file.getvalue(), content_type="application/x-zip-compressed")
        # ..and correct content-disposition
        response['Content-Disposition'] = (
            'attachment; filename="{}-Sponsor-{}.zip"'.format(
                version_obj.project.name, version_obj.name)
        )

        return response

    # noinspection PyMethodMayBeStatic
    def _prepare_zip_archive(self, document, version_obj):
        """Prepare a ZIP file with the document and referenced images.
        :param document:
        :param version_obj: Instance of a version object.

        :returns temporary path for the created zip file
        :rtype: string
        """
        # create in memory file-like object
        temp_path = StringIO.StringIO()

        # grab all of the images from document
        images = []
        page = BeautifulSoup(document, 'html.parser')
        pages = page.findAll('img')
        for image in pages:
            img = image['src']
            images.append(img)

        # create the ZIP file
        with zipfile.ZipFile(temp_path, 'w') as zip_file:
            # write all of the image files (read from disk)
            for image in images:
                zip_file.write(
                    '../media/{0}'.format(image),
                    '{0}'.format(image)
                )
            # write the actual html document
            zip_file.writestr(
                '{}-Sponsor-{}.html'.format(
                    version_obj.project.name, version_obj.name),
                document)

        return temp_path
