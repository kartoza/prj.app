# coding=utf-8
"""**Feed class for Version**
"""

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from base.models.project import Project
from changes.models.version import Version


# noinspection PyMethodMayBeStatic
class VersionFeed(Feed):
    """Feed class for version."""

    def get_object(self, request, *args, **kwargs):
        """Return project object that matches the project_slug."""
        project_slug = kwargs.get('project_slug', None)
        return get_object_or_404(Project, slug=project_slug)

    def title(self, obj):
        """Set the title of the RSS."""
        return 'RSS Version of %s Project' % obj.name

    def description(self, obj):
        """Set the description of the RSS."""
        return 'These are the latest version of %s project.' % obj.name

    def link(self, obj):
        """Set the url of the project."""
        return obj.get_absolute_url()

    def items(self, obj):
        """Return last 5 (if possible) version of the project."""
        return Version.objects.filter(project=obj).order_by(
            '-datetime_created')[:5]

    def item_title(self, item):
        """Return the title of the version."""
        return item.name

    def item_description(self, item):
        """Return the description of the version."""
        return item.description