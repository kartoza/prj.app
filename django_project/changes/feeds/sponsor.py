# coding=utf-8

__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '23/10/2017'

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from base.models.project import Project
from changes.models.sponsorship_period import SponsorshipPeriod


# noinspection PyMethodMayBeStatic
class RssSponsorFeed(Feed):
    """RSS Feed class for sponsor."""

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
        return 'RSS Sponsor of %s Project' % obj.name

    def description(self, obj):
        """Return a description for the RSS.

         :param obj: A project
         :type obj: Project

         :returns: Description of the RSS Feed.
         :rtype: str
         """
        return 'These are the latest sponsor of %s project.' % obj.name

    def link(self, obj):
        """Return the url of the latest sponsor.

        :param obj: Latest sponsor of a project
        :type obj: SponsorshipPeriod

        :returns: Url of the latest sponsor.
        :rtype: str
        """
        return obj.get_absolute_url()

    def items(self, obj):
        """Return latest sponsors of the project.

        :param obj: A project
        :type obj: Project

        :returns: List of latest sponsor of a project
        :rtype: list
        """
        return SponsorshipPeriod.objects.filter(
            project=obj).order_by('-sponsorship_level__value', '-end_date')

    def item_title(self, item):
        """Return the title of the sponsor.

        :param item: Sponsorship period object of a project
        :type item: Sponsorship period

        :returns: name of the sponsor
        :rtype: str
        """
        return item.sponsor.name

    def item_description(self, item):
        """Return the description of the sponsor.

        :param item: Sponsorship period object of a project
        :type item: Sponsorship period

        :returns: description of the sponsor
        :rtype: str
        """
        data = {
            'media_url': settings.MEDIA_URL,
            'sponsor_logo': item.sponsor.logo,
            'sponsor_level': item.sponsorship_level,
            'start_date': item.start_date.strftime('%d %B %Y'),
            'end_date': item.end_date.strftime('%d %B %Y'),
            'currency': item.currency,
            'amount_sponsored': item.amount_sponsored,
        }

        descriptions = \
            '<div>' \
            '<img src="{media_url}{sponsor_logo}" width="300px"></div>' \
            '<p><span>Sponsorship level: {sponsor_level}</span><br/>' \
            '<span>Sponsorship period: {start_date} - {end_date}</span><br/>' \
            '<span>Amount sponsored: {currency} {amount_sponsored}<span></p>'\
            .format(**data)
        return descriptions


class AtomSponsorFeed(RssSponsorFeed):
    """Atom Feed class for sponsor."""

    feed_type = Atom1Feed
    subtitle = RssSponsorFeed.description
