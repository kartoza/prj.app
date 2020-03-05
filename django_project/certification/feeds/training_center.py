# coding=utf-8
from django.contrib.gis.feeds import Feed
from django.http import Http404
from django.shortcuts import get_object_or_404
from base.models.project import Project
from certification.models.certifying_organisation import CertifyingOrganisation
from certification.models.training_center import TrainingCenter
from .geojson_feed import GeoJSONFeed


class TrainingCenterFeed(Feed):
    """Feed for training center."""

    feed_type = GeoJSONFeed

    def get_object(self, request, *args, **kwargs):
        """Return the certifying organisation object that
        matches the project_slug and organisation slug.

        :param request: The incoming HTTP request object
        :type request: Request object

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: certifying organisation
        :rtype: CertifyingOrganisation

        :raises: Http404
        """
        try:
            project_slug = kwargs.get('project_slug', None)
            project = get_object_or_404(Project, slug=project_slug)
            organisation_slug = kwargs.get('organisation_slug', None)
            certifying_organisation = (
                get_object_or_404(
                    CertifyingOrganisation,
                    slug=organisation_slug,
                    project=project
                ))
            certifying_organisation.uri = (
                self.get_absolute_obj_url(request, certifying_organisation))
            return certifying_organisation
        except Http404:
            raise Http404(
                'Sorry! We could not find your '
                'project/certifying organisation!')

    def get_absolute_obj_url(self, request, obj):
        return request.build_absolute_uri(obj.get_absolute_url())

    def title(self, obj):
        """Return a title for the RSS.

         :param obj: A certifying organisation
         :type obj: CertifyingOrganisation

         :returns: Title of the RSS Feed.
         :rtype: str
         """
        return 'GeoJSON Feed training center of {}'.format(obj.name)

    def link(self, obj):
        """Return the url of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: Url of the certifying organisation.
        :rtype: str
        """
        return obj.uri

    def feed_extra_kwargs(self, obj):
        """Return the homepage of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: Homepage of the certifying organisation.
        :rtype: str
        """
        return {
            'homepage': obj.url
        }

    def description(self, obj):
        """Return a description for the RSS.

         :param obj: A certifying organisation
         :type obj: CertifyingOrganisation

         :returns: Description of the RSS Feed.
         :rtype: str
         """
        return 'These are the training center ' \
               'of {}.'.format(obj.name)

    def items(self, obj):
        """Return training center of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: List of training center of a certifying organisation
        :rtype: list
        """
        return TrainingCenter.objects.filter(
            certifying_organisation=obj,
        ).order_by('-name')

    def item_title(self, item):
        """Return the title of the training center.

        :param item: Training center object of a certifying organisation
        :type item: TrainingCenter

        :returns: name of the training center
        :rtype: str
        """
        return item.name

    def item_extra_kwargs(self, item):
        return {
            'location': item.location
        }
