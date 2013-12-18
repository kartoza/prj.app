from django.shortcuts import render_to_response
from django.template import RequestContext
from base.models import Project, Version
from changes.models import Entry, Category
from vota.models import Committee, Ballot


def navigation_view(request):
    the_project = None
    projects = None
    versions = None
    the_version = None
    the_committee = None
    committees = None
    ballots = None
    entries = None
    categories = None
    if request.GET.get('project_slug', None):
        the_project = Project.objects.get(slug=request.GET.get('project_slug'))
        projects = Project.approved_objects.all()
        # We don't want to see committees under versions
        if not request.GET.get('version_slug', None):
            committees = Committee.objects.filter(project=the_project)
        # We don't want to see versions under committees
        if not request.GET.get('committee_slug', None):
            versions = Version.objects.filter(project=the_project)
    if request.GET.get('committee_slug', None):
        the_committee = Committee.objects.get(
            slug=request.GET.get('committee_slug'))
        ballots = Ballot.objects.filter(committee=the_committee)
    if request.GET.get('version_slug', None):
        if not request.user.is_staff:
            the_version = Version.objects.get(
                slug=request.GET.get('version_slug'))
        else:
            the_version = Version.approved_objects.get(
                slug=request.GET.get('version_slug'))
        if not request.user.is_staff:
            # Only show the 10 most recent entries
            entries = Entry.approved_objects.filter(version=the_version)[:10]
        else:
            # Only show the 10 most recent entries
            entries = Entry.objects.filter(version=the_version)[:10]
        if the_project:
            if not request.user.is_staff:
                categories = Category.objects.filter(
                    project=the_project)
            else:
                categories = Category.approved_objects.filter(
                    project=the_project)
        else:
            if not request.user.is_staff:
                categories = Category.approved_objects.filter(
                    project=the_version.project)
            else:
                categories = Category.objects.filter(
                    project=the_version.project)

    return render_to_response('navigation.html', {
        'the_project': the_project,
        'projects': projects,
        'versions': versions,
        'the_version': the_version,
        'the_committee': the_committee,
        'committees': committees,
        'ballots': ballots,
        'entries': entries,
        'categories': categories,
    }, context_instance=RequestContext(request))
