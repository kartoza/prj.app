from django.core.urlresolvers import reverse


class NavContextMiddleware:
    """
    Adds the required nav_url to each response.

    :arg: project
    :return: If present in response.context (which it should be in nearly every
        view except Home), all the Organisation's Projects will be shown in the
        menu under the current project's name.

    :arg: committee
    :return: If present in response.context, the user is in the vota app and
        will see a list of authorised committees and their ballots in the menu.

    :arg: version
    :return: If present in response.context, the user is in the changes app and
        will see a list of the project's versions, categories and entries
    """
    def process_template_response(self, request, response):
        context = response.context_data
        nav_url = '%s?' % reverse('nav')
        if context.get('project', None):
            nav_url += 'project_slug=%s' % context['project'].slug
        if context.get('committee', None):
            committee = context['committee']
            nav_url += 'project_slug=%s&committee_slug=%s' % (
                committee.project.slug, committee.slug
            )
        if context.get('version', None):
            version = context['version']
            nav_url += 'project_slug=%s&version_slug=%s' % (
                version.project.slug, version.slug,
            )
        if context.get('entry', None):
            entry = context['entry']
            version = entry.version
            nav_url += 'project_slug=%s&version_slug=%s' % (
                version.project.slug, version.slug,
            )
        response.context_data['nav_url'] = nav_url
        return response
