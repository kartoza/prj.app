# coding=utf-8
"""**Feed class for Entry**
"""

__author__ = 'Ismail Sunni <ismail@linfiniti.com>'
__revision__ = '$Format:%H$'
__date__ = '15/04/2014'
__license__ = ''
__copyright__ = ''

from django.contrib.syndication.views import Feed
from django.shortcuts import get_list_or_404
from django.http import Http404
from base.models.project import Project
from changes.models.version import Version
from changes.models.entry import Entry


# noinspection PyMethodMayBeStatic
class EntryFeed(Feed):
    """Feed class for Entry."""

    def get_object(self, request, *args, **kwargs):
        """Return project object that matches the project_slug."""
        try:
            project_slug = kwargs.get('project_slug', None)
            project = Project.objects.get(slug=project_slug)
            version = get_list_or_404(Version.objects.order_by(
                '-datetime_created'), project=project, approved=True)[0]
            return version
        except Http404:
            raise Http404('Sorry! We could not find your project!')

    def title(self, obj):
        """Set the title of the RSS."""
        return 'RSS Entry of %s Project\'s latest version' % obj.project.name

    def description(self, obj):
        """Set the description of the RSS."""
        return ('These are the entries from the latest version of %s project.'
                % obj.project.name)

    def link(self, obj):
        """Set the url of the project."""
        return obj.get_absolute_url()

    def items(self, obj):
        """Return all entries form the latest version of a project.

        Only for approved version and entry.
        """
        return Entry.objects.filter(version=obj, approved=True).order_by(
            '-datetime_created')

    def item_title(self, item):
        """Return the title of the version."""
        return item.title

    def item_description(self, item):
        """Return the description of the version."""
        return item.description