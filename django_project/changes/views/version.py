# -*- coding: utf-8 -*-
"""**View classes for Version**

"""

# noinspection PyUnresolvedReferences
# import logging
from base.models import Project
# LOGGER = logging.getLogger(__name__)
import re
import zipfile
from io import BytesIO
import pypandoc
from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Q
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


class CustomStaffuserRequiredMixin(StaffuserRequiredMixin):

    """Fix redirect loop when user is already authenticated but non staff."""

    def no_permissions_fail(self, request=None):
        """
        Called when the user has no permissions and no exception was raised.
        """
        if not request.user.is_authenticated:
            return super(
                CustomStaffuserRequiredMixin, self).no_permissions_fail(
                request)

        raise Http404('Sorry! You have to be staff to open this page.')


class VersionListView(VersionMixin, PaginationMixin, ListView):
    """List view for Version."""
    context_object_name = 'versions'
    template_name = 'version/list.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(VersionListView, self).get_context_data(**kwargs)

        # lets set the the flags to a default
        # for running checks in templates
        context['user_can_edit'] = False
        context['user_can_delete'] = False

        context['num_versions'] = self.get_queryset().count()
        context['rst_download'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['the_project'] = Project.objects.get(slug=project_slug)
            context['project'] = context['the_project']

        # lets check for specific user permissions here.
        if self.request.user.is_staff:
            context['user_can_edit'] = True
            context['user_can_delete'] = True

        if self.request.user.is_superuser:
            context['user_can_edit'] = True
            context['user_can_delete'] = True

        if self.request.user in context['project'].changelog_managers.all():
            context['user_can_edit'] = True
            context['user_can_delete'] = True

        if self.request.user == context['project'].owner:
            context['user_can_edit'] = True
            context['user_can_delete'] = True

        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which show all Version for this project.
        :rtype: QuerySet

        :raises: Http404
        """
        versions_qs = Version.objects.all()

        # fix padded version if there is padded name with alphabet.
        for version in versions_qs:
            is_alphabet = re.search('[a-zA-Z,.]', str(version.padded_version))
            if is_alphabet is not None:
                version.save()

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


class VersionDetailView(VersionMixin, DetailView):
    """A tabular list style view for a Version."""
    context_object_name = 'version'
    template_name = 'version/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(VersionDetailView, self).get_context_data(**kwargs)
        versions = self.get_object()
        sponsors = {}

        # group sponsors by sponsorship level
        if versions.sponsors():
            for sponsor in versions.sponsors():
                if sponsor.sponsorship_level not in sponsors:
                    sponsors[sponsor.sponsorship_level] = []

                sponsors[sponsor.sponsorship_level].append(sponsor.sponsor)

        context['sponsors'] = sponsors
        context['user_can_edit'] = False
        context['user_can_delete'] = False
        project_slug = self.kwargs.get('project_slug', None)
        context['project_slug'] = project_slug
        if project_slug:
            context['project'] = Project.objects.get(slug=project_slug)

        # lets check for specific user permissions here.
        if self.request.user.is_staff:
            context['user_can_edit'] = True
            context['user_can_delete'] = True

        if self.request.user.is_superuser:
            context['user_can_edit'] = True
            context['user_can_delete'] = True

        if self.request.user in context['project'].changelog_managers.all():
            context['user_can_edit'] = True
            context['user_can_delete'] = True

        if self.request.user == context['project'].owner:
            context['user_can_edit'] = True
            context['user_can_delete'] = True
        return context

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
                    'view the version. Try logging in as a staff member if '
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
                    'view the version. Try logging in as a staff member if '
                    'you wish to view it.')
            try:
                obj = queryset.filter(project=project).get(slug=slug)
                return obj
            except Version.DoesNotExist:
                raise Http404(
                    'Sorry! The version you are requesting '
                    'could not be found or you do not have permission to '
                    'view the version. Try logging in as a staff member if '
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
        project_slug = self.kwargs.get('project_slug', None)
        project = Project.objects.get(slug=project_slug)
        if not self.request.user.is_authenticated:
            raise Http404
        qs = Version.objects.filter(project=project, locked=False)
        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(
                Q(project=project) &
                (Q(author=self.request.user) |
                 Q(project__owner=self.request.user) |
                 Q(project__changelog_managers=self.request.user))).distinct()


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
        to the Version list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('version-list', kwargs={
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
class VersionUpdateView(LoginRequiredMixin, VersionMixin, UpdateView):
    """Update view for Version."""
    context_object_name = 'version'
    template_name = 'version/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(VersionUpdateView, self).get_form_kwargs()
        project_slug = self.kwargs.get('project_slug', None)
        kwargs['user'] = self.request.user
        kwargs['project'] = get_object_or_404(Project, slug=project_slug)
        return kwargs

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show versions that the
        current user can potentially edit.
        :rtype: QuerySet
        """
        project_slug = self.kwargs.get('project_slug', None)
        project = get_object_or_404(Project, slug=project_slug)
        # Versions are uniques only within the same project.
        versions_qs = Version.objects.filter(project=project, locked=False)
        if not self.request.user.is_staff:
            versions_qs = versions_qs.filter(
                (Q(author=self.request.user) |
                 Q(project__owner=self.request.user) |
                 Q(project__changelog_managers=self.request.user))).distinct()
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


class VersionDownload(CustomStaffuserRequiredMixin, VersionMixin, DetailView):
    """View to allow staff users to download Version page in RST format."""
    template_name = 'version/detail-content-rst.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(VersionDownload, self).get_context_data(**kwargs)
        versions = self.get_object()
        sponsors = {}

        # group sponsors by sponsorship level
        if versions.sponsors():
            for sponsor in versions.sponsors():
                if sponsor.sponsorship_level not in sponsors:
                    sponsors[sponsor.sponsorship_level] = []

                sponsors[sponsor.sponsorship_level].append(sponsor.sponsor)

        context['sponsors'] = sponsors
        return context

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
            document.rendered_content.encode('utf8', 'ignore'),
            'rst', format='html', extra_args=['--no-wrap'])
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
        temp_path = BytesIO()

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
                try:
                    image_url = '{}/{}'.format(settings.MEDIA_ROOT, image)
                    zip_file.write(
                        image_url,
                        '{0}'.format(image)
                    )
                except FileNotFoundError:
                    pass
            # write the actual RST document
            zip_file.writestr(
                'index.rst',
                document)

        return temp_path

    def get_queryset(self):
        """Get the queryset for download.

        This will search a specific version within a project.
        Thus it will not raise duplicates when there is
        another same version name from another project.

        :returns: A queryset which is filtered to only show Version
        from specific project.
        :rtype: QuerySet
        :raises: Http404
        """

        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            slug = self.kwargs.get('slug', None)
            if project_slug and slug:
                try:
                    project = Project.objects.get(slug=project_slug)
                    queryset = Version.objects.filter(
                        project=project, slug=slug)
                    return queryset
                except (Project.DoesNotExist, Version.DoesNotExist):
                    raise Http404('Sorry! We could not find your version!')
            else:
                raise Http404('Sorry! We could not find your version!')
        return self.queryset


class VersionDownloadMd(VersionMixin, DetailView):
    """View to allow users to download Version page in Markdown format."""
    template_name = 'version/detail-content-md.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(VersionDownloadMd, self).get_context_data(**kwargs)
        versions = self.get_object()
        sponsors = {}

        # group sponsors by sponsorship level
        if versions.sponsors():
            for sponsor in versions.sponsors():
                if sponsor.sponsorship_level not in sponsors:
                    sponsors[sponsor.sponsorship_level] = []

                sponsors[sponsor.sponsorship_level].append(sponsor.sponsor)

        context['sponsors'] = sponsors
        return context

    def render_to_response(self, context, **response_kwargs):
        """Returns a Markdown document for a project Version page.

        :param context:
        :type context: dict

        :param response_kwargs: Keyword Arguments
        :param response_kwargs: dict

        :returns: a Markdown document for a project Version page.
        :rtype: HttpResponse
        """
        version_obj = context.get('version')
        # set the context flag for 'md_download'
        context['md_download'] = True
        # render the template
        document = self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )

        # convert the html to markdown
        converted_doc = pypandoc.convert(
            document.rendered_content.encode('utf8', 'ignore'),
            'md', format='html', extra_args=['--no-wrap'])
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

    def _convert_headers(self, markdown_content):
        """
        Convert underlined sections in a Markdown document to proper headers.

        Sections underlined with '=' become first-level headers '#'
        Sections underlined with '-' become second-level headers '##'

        Args:
            markdown_content (str): The original Markdown content.

        Returns:
            str: The transformed Markdown content with headers.
        """
        # Define patterns for first and second-level headers
        first_level_pattern = r'^(.*)\n=+\n'
        second_level_pattern = r'^(.*)\n-+\n'

        # Replace first-level underlined sections with '#'
        markdown_content = re.sub(
            first_level_pattern,
            r'# \1\n',
            markdown_content,
            flags=re.MULTILINE
        )

        # Replace second-level underlined sections with '##'
        markdown_content = re.sub(
            second_level_pattern,
            r'## \1\n',
            markdown_content,
            flags=re.MULTILINE
        )

        return markdown_content

    # noinspection PyMethodMayBeStatic
    def _prepare_zip_archive(self, document, version_obj):
        """Prepare a ZIP file with the document and referenced images.

        :param document:
        :param version_obj: Instance of a version object.

        :returns temporary path for the created zip file
        :rtype: string
        """
        # create in memory file-like object
        temp_path = BytesIO()

        # Convert headers
        document = self._convert_headers(document)
        # Remove CSS styles and classes
        document = re.sub(r'\{.*?\}', '', document)
        # Regular expression pattern for Markdown image syntax
        pattern = re.compile(r'!\[.*?\]\((.*?)\)')
        # Find all matches
        images = pattern.findall(document)
        if not images:
            images = []

        # create the ZIP file
        with zipfile.ZipFile(temp_path, 'w') as zip_file:
            # write all of the image files (read from disk)
            for image in images:
                try:
                    image_url = '{}/{}'.format(settings.MEDIA_ROOT, image)
                    zip_file.write(
                        image_url,
                        '{0}'.format(image)
                    )
                except FileNotFoundError:
                    pass
            # write the actual Markdown document
            zip_file.writestr(
                'index.md',
                document)
        return temp_path

    def get_queryset(self):
        """Get the queryset for download.

        This will search a specific version within a project.
        Thus it will not raise duplicates when there is
        another same version name from another project.

        :returns: A queryset which is filtered to only show Version
        from specific project.
        :rtype: QuerySet
        :raises: Http404
        """

        if self.queryset is None:
            project_slug = self.kwargs.get('project_slug', None)
            slug = self.kwargs.get('slug', None)
            if project_slug and slug:
                try:
                    project = Project.objects.get(slug=project_slug)
                    queryset = Version.objects.filter(
                        project=project, slug=slug)
                    return queryset
                except (Project.DoesNotExist, Version.DoesNotExist):
                    raise Http404('Sorry! We could not find your version!')
            else:
                raise Http404('Sorry! We could not find your version!')
        return self.queryset


class VersionDownloadGnu(VersionMixin, DetailView):
    """A tabular list style view for a Version."""
    context_object_name = 'version'
    template_name = 'version/detail-titles.txt'

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
                    'view the version. Try logging in as a staff member if '
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


class VersionSponsorDownload(
    CustomStaffuserRequiredMixin, VersionMixin, DetailView):

    """View to allow staff users to download Version page in html format."""

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
            'attachment; filename="{}-SustainingMember-{}.zip"'.format(
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
        temp_path = BytesIO()

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
                '{}-SustainingMember-{}.html'.format(
                    version_obj.project.name, version_obj.name),
                document)

        return temp_path
