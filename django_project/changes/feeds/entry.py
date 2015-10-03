# coding=utf-8
"""**Feed class for Entry**
"""

__author__ = 'Ismail Sunni <ismail@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '15/04/2014'
__license__ = ''
__copyright__ = ''

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_list_or_404
from django.http import Http404
from base.models.project import Project
from changes.models.version import Version
from changes.models.entry import Entry
from django.conf import settings


# noinspection PyMethodMayBeStatic
class RssEntryFeed(Feed):
    """RSS Feed class for Entry."""

    def get_object(self, request, *args, **kwargs):
        """Return the latest Version object that matches the project_slug.

        :param request: The incoming HTTP request object
        :type request: Request object

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: latest version of a project
        :rtype: Version

        :raises: Http404
        """
        try:
            project_slug = kwargs.get('project_slug', None)
            project = Project.objects.get(slug=project_slug)
            version_slug = kwargs.get('version_slug', None)
            # Check if version is given, give atom for the that version,
            # otherwise give the latest version.
            if version_slug is None:
                version = get_list_or_404(Version.objects.order_by(
                    '-datetime_created'), project=project, approved=True)[0]
            else:
                version = Version.objects.get(slug=version_slug)
            return version
        except Http404:
            raise Http404('Sorry! We could not find your project!')

    def title(self, obj):
        """Return a title for the RSS.

        :param obj: Latest version of a project
        :type obj: Version

        :returns: Title of the RSS Feed.
        :rtype: str
        """
        return 'RSS Entry of %s Project\'s latest version' % obj.project.name

    def description(self, obj):
        """Return a description for the RSS.

        :param obj: Latest version of a project
        :type obj: Version

        :returns: Description of the RSS Feed.
        :rtype: str
        """
        return ('These are the entries from the latest version of %s project.'
                % obj.project.name)

    def link(self, obj):
        """Return the url of the latest version.

        :param obj: Latest version of a project
        :type obj: Version

        :returns: Url of the latest version.
        :rtype: str
        """
        return obj.get_absolute_url()

    def items(self, obj):
        """Return all entries form the latest version of a project.

        Only for approved version and entry.

        :param obj: Latest version of a project
        :type obj: Version

        :returns: List of approved entry from the latest version of a project
        :rtype: list
        """
        return Entry.objects.filter(version=obj, approved=True).order_by(
            '-datetime_created')

    def item_title(self, item):
        """Return the title of the entry.

        :param item: Entry object from the latest version of a project
        :type item: Entry

        :returns: title of the entry
        :rtype: str
        """
        return item.title

    def item_description(self, item):
        """Return the description of the entry.

        :param item: Entry object from the latest Version of a Project
        :type item: Entry

        :returns: description of the Entry
        :rtype: str
        """
        return '<p>' + item.description + \
               '</p><p><img src="' + settings.MEDIA_URL + \
               item.image_file.name + '"/></p>'

class AtomEntryFeed(RssEntryFeed):
    """Atom Feed class for Entry."""
    feed_type = Atom1Feed
    subtitle = RssEntryFeed.description
