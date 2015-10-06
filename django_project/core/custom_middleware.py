# coding=utf-8
# flake8: noqa
"""
core.custom_middleware
"""
from base.models import Project


class NavContextMiddleware(object):
    """
    Adds the required navigation variables to each response
    """

    def __init__(self):
        pass

    @staticmethod
    def process_template_response(request, response):
        """
        Add 'the_project', 'the_entry', 'the_version' to context for the
            navigation.

        Justification: To make the navigation functional, we need to know
            which Project (or Version, Committee etc) the current context
            relates to. This is required for URLs. Rather than include lots of
            if/else in the navigation template, it seems cleaner to add the
            above variables to the context here.

        :param request: Http Request obj
        :param response: Http Response obj
        :return: context :rtype: dict
        """
        context = response.context_data

        if context.get('project', None):
            context['the_project'] = context.get('project')
        else:
            if request.user.is_staff:
                context['the_projects'] = Project.objects.all()
            else:
                context['the_projects'] = Project.approved_objects.filter(
                    private=False
                )

        if context.get('version', None):
            context['the_version'] = context.get('version')
            context['the_project'] = context.get('version').project

        if context.get('committee', None):
            context['the_committee'] = context.get('committee')
            context['the_project'] = context.get('committee').project

        if context.get('ballot', None):
            context['the_committee'] = context.get('ballot').committee
            context['the_project'] = context.get('ballot').committee.project

        if context.get('category', None):
            context['the_project'] = context.get('category').project

        if context.get('ballots', None):
            try:
                context['the_project'] = \
                    context.get('ballots')[0].committee.project
            except (KeyError, IndexError):
                pass

        if context.get('entry', None):
            context['the_entry'] = context.get('entry')
            context['the_version'] = context.get('entry').version
            context['the_project'] = context.get('entry').version.project

        if context.get('committees', None):
            try:
                context['the_project'] = context.get('committees')[0].project
            except (KeyError, IndexError):
                pass

        if context.get('versions', None):
            try:
                context['the_project'] = context.get('versions')[0].project
            except (KeyError, IndexError):
                pass

        if context.get('entries', None):
            try:
                context['the_version'] = context.get('entries')[0].version
                context['the_project'] = \
                    context.get('entries')[0].version.project
            except (KeyError, IndexError):
                pass

        if context.get('categories', None):
            try:
                context['the_project'] = \
                    context.get('categories')[0].project
            except (KeyError, IndexError):
                pass

        return response
