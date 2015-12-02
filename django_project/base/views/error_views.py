# coding=utf-8
"""Our custom error views"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from base.models.project import Project


def custom_404(request, template_name='404.html'):
    """Our custom 404 view

    We want to include a list of all public and approved Projects in the 404
        view
    :param request: Request obj
    :type request: HttpRequest

    :param template_name: The template to render
    :type template_name: str

    :return: Response obj
    :rtype: HttpResponse

    """
    public_projects = Project.objects.filter(approved=True, private=False)

    response = render_to_response(template_name, {
        'request_path': request.path,
        'projects': public_projects},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

