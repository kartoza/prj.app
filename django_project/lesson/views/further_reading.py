# coding=utf-8
"""Further reading views."""

import json
import requests

from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from base.models.project import Project
from lesson.models.further_reading import FurtherReading
from lesson.models.worksheet import Worksheet
from lesson.forms.further_reading import FurtherReadingForm
from lesson.utilities import GetAllFurtherReadingLink


class FurtherReadingMixin(object):
    """Mixin class to provide standard settings for Further Reading."""

    model = FurtherReading
    form_class = FurtherReadingForm


class FurtherReadingCreateView(
    LoginRequiredMixin, FurtherReadingMixin, CreateView):
    """Create view for Further Reading."""

    context_object_name = 'further_reading'
    template_name = 'create.html'
    creation_label = _('Add further reading item')

    def get_success_url(self):
        """Define the redirect URL

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.worksheet.pk,
            'section_slug': self.object.worksheet.section.slug,
            'project_slug': self.object.worksheet.section.project.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(FurtherReadingCreateView, self).get_form_kwargs()
        worksheet_slug = self.kwargs['worksheet_slug']
        kwargs['worksheet'] = get_object_or_404(Worksheet, slug=worksheet_slug)
        return kwargs


# noinspection PyAttributeOutsideInit
class FurtherReadingDeleteView(
        LoginRequiredMixin,
        FurtherReadingMixin,
        DeleteView):
    """Delete view for Further reading."""

    context_object_name = 'further_reading'
    template_name = 'further_reading/delete.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation list page
        for the object's parent Worksheet.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('worksheet-detail', kwargs={
            'pk': self.object.worksheet.pk,
            'section_slug': self.object.worksheet.section.slug,
            'project_slug': self.object.worksheet.section.project.slug
        })


# noinspection PyAttributeOutsideInit
class FurtherReadingUpdateView(
        LoginRequiredMixin,
        FurtherReadingMixin,
        UpdateView):
    """Update view for Further Reading."""

    context_object_name = 'further_reading'
    template_name = 'update.html'
    update_label = _('Update further reading item')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(FurtherReadingUpdateView, self).get_form_kwargs()
        worksheet_slug = self.kwargs.get('worksheet_slug', None)
        kwargs['worksheet'] = get_object_or_404(Worksheet, slug=worksheet_slug)
        return kwargs

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the specification list page for the object's parent Worksheet.

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.worksheet.pk,
            'section_slug': self.object.worksheet.section.slug,
            'project_slug': self.object.worksheet.section.project.slug
        })


def get_FurtherReading_links(request, **kwargs):

    project_slug = kwargs.get('project_slug', None)
    if not project_slug:
        return JsonResponse({'data': None})

    project = Project.objects.get(slug=project_slug)
    if not project:
        return JsonResponse({'data': None})

    invalid_links_list = GetAllFurtherReadingLink(
        project).get_all_url()

    return JsonResponse({
        'data': invalid_links_list,
        'project_slug': project_slug,
        'project_name': project.name
    })


def print_invalid_FurterReading_links(request, **kwargs):
    project_slug = kwargs.get('project_slug', None)
    data = request.GET.get('data')
    if data:
        data = json.loads(data)

    from changes.utils.render_to_pdf import render_to_pdf
    pdf = render_to_pdf(
        'further_reading/print_invalid_links.html', data)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'Invalid_FurtherReading_{project_slug}.pdf'
    content = "inline; filename='%s'" % (filename)
    download = request.GET.get("download")
    if download:
        content = "attachment; filename='%s'" % (filename)
    response['Content-Disposition'] = content
    return response


def is_url_exist(request, **kwargs):
    url_string = request.GET.get('url_string')
    if not url_string:
        return JsonResponse({'is_url_exist': False, 'url': url_string})
    try:
        req = requests.head(url_string)
    except requests.exceptions.SSLError:
        req = requests.head(url_string, verify=False)
    except Exception:
        return JsonResponse({'is_url_exist': False, 'url': url_string})
    if req.status_code >= 400:
        return JsonResponse({'is_url_exist': False, 'url': url_string})
    return JsonResponse({'is_url_exist': True, 'url': url_string})
