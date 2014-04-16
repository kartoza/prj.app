# coding=utf-8
"""**Feed class for Version**
"""

__author__ = 'Ismail Sunni <ismail@linfiniti.com>'
__revision__ = '$Format:%H$'
__date__ = '14/04/2014'
__license__ = ''
__copyright__ = ''

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from base.models.project import Project
from changes.models.version import Version


# noinspection PyMethodMayBeStatic
class VersionFeed(Feed):
    """Feed class for version."""

    def get_object(self, request, *args, **kwargs):
        """Return project object that matches the project_slug.

        :param request: The incoming HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: A project
        :rtype: Project

        :raises: Http404
        """
        project_slug = kwargs.get('project_slug', None)
        return get_object_or_404(Project, slug=project_slug)

    def title(self, obj):
        """Return a title for the RSS.

         :param obj: A project
         :type obj: Project

         :returns: Title of the RSS Feed.
         :rtype: str
         """
        return 'RSS Version of %s Project' % obj.name

    def description(self, obj):
        """Return a description for the RSS.

         :param obj: A project
         :type obj: Project

         :returns: Description of the RSS Feed.
         :rtype: str
         """
        return 'These are the latest version of %s project.' % obj.name

    def link(self, obj):
        """Return the url of the latest version.

        :param obj: Latest version of a project
        :type obj: Version

        :returns: Url of the latest version.
        :rtype: str
        """
        return obj.get_absolute_url()

    def items(self, obj):
        """Return last 5 (if possible) version of the project.

        :param obj: A project
        :type obj: Project

        :returns: List of approved version of a project
        :rtype: list
        """
        return Version.objects.filter(project=obj, approved=True).order_by(
            '-datetime_created')[:5]

    def item_title(self, item):
        """Return the title of the version.

        :param item: Version object of a project
        :type item: Version

        :returns: title of the Version
        :rtype: str
        """
        return item.name

    def item_description(self, item):
        """Return the description of the version.

        :param item: Version object of a project
        :type item: Version

        :returns: description of the Version
        :rtype: str
        """
        return item.description
