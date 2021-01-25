from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import DEFAULT_TEMPLATE
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.utils import translation
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from base.models import Project, ProjectFlatpage


def general_flatpage(request, url):
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
        f = get_object_or_404(FlatPage, url=url, sites=site_id)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(FlatPage, url=url, sites=site_id)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_custom_general_flatpage(request, f)


@csrf_protect
def render_custom_general_flatpage(request, f):
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
    project_flatpage_ids = (
        ProjectFlatpage.objects.all().values_list('id', flat=True))
    flatpages = FlatPage.objects.exclude(id__in=project_flatpage_ids)
    if request.user.is_staff:
        the_projects = Project.objects.all()
    else:
        the_projects = Project.approved_objects.filter(
            private=False
        )

    response = HttpResponse(
        template.render({
            'flatpage': f,
            'flatpages': flatpages,
            'the_projects': the_projects
        }, request))
    return response


def index_view(request):
    user_language = (translation.get_language() or
                     settings.LANGUAGE_CODE or 'en')
    translation.activate(user_language)
    # look up the view name in base.urls
    return redirect(reverse('home'))
