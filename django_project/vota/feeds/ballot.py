# coding=utf-8
"""**Feed class for Ballot**
"""

__author__ = 'Ismail Sunni <ismail@linfiniti.com>'
__revision__ = '$Format:%H$'
__date__ = '16/04/2014'
__license__ = ''
__copyright__ = ''

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.http import Http404
from base.models.project import Project
from vota.models.committee import Committee
from vota.models.ballot import Ballot


# noinspection PyMethodMayBeStatic
class BallotFeed(Feed):
    """Feed class for Ballot."""

    def get_object(self, request, *args, **kwargs):
        """Return the a Committee object.

        It must match with project_slug and committee_slug

        :param request: The incoming HTTP request object
        :type request: Request object

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: A Committee of a project
        :rtype: Committee

        :raises: Http404
        """
        try:
            project_slug = kwargs.get('project_slug', None)
            project = Project.objects.get(slug=project_slug)
            committee_slug = kwargs.get('committee_slug', None)
            committee = get_object_or_404(
                Committee, project=project, slug=committee_slug)
            return committee
        except Http404:
            raise Http404('Sorry! We could not find your Committee!')

    def title(self, obj):
        """Return a title for the RSS.

        :param obj: A committee project
        :type obj: Committee

        :returns: Title of the RSS Feed.
        :rtype: str
        """
        return ('RSS Ballots of Committee %s from %s Project' % (
            obj.name, obj.project.name))

    def description(self, obj):
        """Return a description for the RSS.

        :param obj: A project Committee
        :type obj: Committee

        :returns: Description of the RSS Feed.
        :rtype: str
        """
        return ('These are the latest ballots from Committee %s of version of '
                '%s project.' % (obj.name, obj.project.name))

    def link(self, obj):
        """Return the url of the Committee.

        :param obj: A project Committee
        :type obj: Committee

        :returns: Url of the latest version.
        :rtype: str
        """
        return obj.get_absolute_url()

    def items(self, obj):
        """Return 5 latest Ballots from a committee of a project.

        Only for approved Ballot and Committee

        :param obj: A committee project
        :type obj: Committee

        :returns: List of 5 latest approved Ballot from a Committee
        :rtype: list
        """
        ballots = Ballot.objects.filter(committee=obj).order_by(
            '-datetime_created')
        return ballots

    def item_title(self, item):
        """Return the title of the Ballot.

        :param item: Approved Ballot from a Committee
        :type item: Ballot

        :returns: title of the Ballot
        :rtype: str
        """
        return item.name

    def item_description(self, item):
        """Return the description of the Ballot.

        :param item: Approved Ballot from a Committee
        :type item: Ballot

        :returns: description of the Ballot
        :rtype: str
        """
        return item.description
