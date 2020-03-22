from django.conf import settings
from django.contrib.flatpages.views import DEFAULT_TEMPLATE
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from .project import Project
from ..models.custom_flatpage import ProjectFlatpage


def project_flatpage(request, url, project_slug):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.startswith('/'):
        url = '/' + url
    site_id = get_current_site(request).id
    try:
        project = get_object_or_404(Project, slug=project_slug)
    except Http404:
        raise

    try:
        f = get_object_or_404(
            ProjectFlatpage, url=url, sites=site_id, project=project)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(
                ProjectFlatpage, url=url, sites=site_id, project=project)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_custom_project_flatpage(request, f, project)


@csrf_protect
def render_custom_project_flatpage(request, f, project):
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        template = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)
    project_flatpages = ProjectFlatpage.objects.filter(
        project=project
    )

    response = HttpResponse(
        template.render({
            'flatpage': f,
            'the_project': project,
            'project_flatpages': project_flatpages
        }, request))
    return response
