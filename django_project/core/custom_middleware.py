from django.core.urlresolvers import reverse
from django.template import loader, Context, Template
from bs4 import BeautifulSoup
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import SimpleTemplateResponse
from django.utils.html import format_html
from django.utils.safestring import SafeText, SafeString, mark_safe
from base.models import Project, Version
from changes.models import Entry, Category
from vota.models import Committee, Ballot
import logging
logger = logging.getLogger(__name__)


def navigation_view(project=None,
                    committee=None,
                    version=None,
                    entry=None,
                    the_entries=None,
                    ballot=None,
                    category=None,
                    the_categories=None,
                    is_staff=False):
    the_version = None
    the_committee = None
    committees = None
    the_ballot = None
    ballots = None
    the_entry = None
    entries = None
    the_project = None
    versions = None
    categories = None
    projects = Project.approved_objects.all()
    if project:
        the_project = project
        # We don't want to see committees under versions
        if not version:
            committees = Committee.objects.filter(project=the_project)
        # We don't want to see versions under committees
        if not committee:
            versions = Version.objects.filter(project=the_project)
    if committee:
        the_committee = committee
        the_project = the_committee.project
        committees = Committee.objects.filter(project=the_project)
        ballots = Ballot.objects.filter(committee=the_committee)
    if version:
        the_version = version
        if not is_staff:
            # Only show the 10 most recent entries
            entries = Entry.approved_objects.filter(version=the_version)[:10]
        else:
            # Only show the 10 most recent entries
            entries = Entry.objects.filter(version=the_version)[:10]
        if not is_staff:
            categories = Category.approved_objects.filter(
                project=the_version.project)
        else:
            categories = Category.objects.filter(
                project=the_version.project)
        the_project = the_version.project
    if category:
        the_project = category.project
        if is_staff:
            versions = Version.objects.filter(project=the_project)
        else:
            versions = Version.approved_objects.filter(project=the_project)
        if not is_staff:
            categories = Category.approved_objects.filter(project=the_project)
        else:
            categories = Category.objects.filter(project=the_project)
    if the_categories:
        first_category = the_categories[0]
        categories = the_categories[:10]
        the_project = first_category.project
        versions = Version.objects.filter(project=the_project)
    if entry:
        the_entry = entry
        entries = Entry.approved_objects.filter(version=entry.version)[:10]
        the_project = entry.version.project
        the_version = entry.version
        if is_staff:
            versions = Version.objects.filter(project=the_project)
        else:
            versions = Version.approved_objects.filter(project=the_project)
        if not is_staff:
            categories = Category.approved_objects.filter(
                project=entry.version.project)
        else:
            categories = Category.objects.filter(
                project=entry.version.project)
    if the_entries:
        first_entry = the_entries[0]
        entries = the_entries[:10]
        the_project = first_entry.version.project
        the_version = first_entry.version
        versions = Version.objects.filter(
            project=first_entry.version.project)
        if not is_staff:
            categories = Category.approved_objects.filter(
                project=first_entry.version.project)
        else:
            categories = Category.objects.filter(
                project=first_entry.version.project)
    if ballot:
        the_ballot = ballot
        ballots = Ballot.objects.filter(committee=ballot.committee)
        the_project = ballot.committee.project
        committees = Committee.objects.filter(project=the_project)

    return {
        'the_project': the_project,
        'projects': projects,
        'versions': versions,
        'the_version': the_version,
        'the_committee': the_committee,
        'committees': committees,
        'the_ballot': the_ballot,
        'ballots': ballots,
        'the_entry': the_entry,
        'entries': entries,
        'categories': categories,
    }


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
        project = None
        committee = None
        version = None
        entry = None
        entries = None
        ballot = None
        category = None
        categories = None
        is_staff = request.user.is_staff
        if not request.path.startswith(reverse('admin:index')):
            if context.get('project', None):
                project = context['project']
            if context.get('committee', None):
                committee = context['committee']
            if context.get('version', None):
                version = context['version']
            if context.get('entry', None):
                entry = context['entry']
            if context.get('entries', None):
                entries = context['entries']
            if context.get('ballot', None):
                ballot = context['ballot']
            if context.get('category', None):
                category = context['category']
            if context.get('categories', None):
                categories = context['categories']
            nav_template = loader.get_template('navigation.html')
            render_nav = navigation_view(
                project=project,
                committee=committee,
                version=version,
                entry=entry,
                the_entries=entries,
                ballot=ballot,
                category=category,
                the_categories=categories,
                is_staff=is_staff
            )
            nav_context = Context(render_nav)
            nav_rendered = nav_template.render(nav_context)
            soup = BeautifulSoup(response.rendered_content)
            container = soup.find(id="nav-souped-content")
            container.insert(1, BeautifulSoup(nav_rendered))
            response.content = mark_safe(soup)
        return response
