# coding=utf-8
"""Worksheet views."""

import json
import StringIO
import os
import zipfile
from collections import OrderedDict
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin
from weasyprint import HTML

from lesson.forms.worksheet import WorksheetForm
from lesson.models.answer import Answer
from lesson.models.further_reading import FurtherReading
from lesson.models.specification import Specification
from lesson.models.worksheet import Worksheet
from lesson.models.worksheet_question import WorksheetQuestion
from lesson.utilities import re_order_features

from base.models.project import Project
from ..models.section import Section


class WorksheetMixin(object):
    """Mixin class to provide standard settings for Worksheet."""

    model = Worksheet
    form_class = WorksheetForm


class WorksheetDetailView(
        WorksheetMixin,
        DetailView):
    """Detail view for worksheet."""

    context_object_name = 'worksheet'
    template_name = 'worksheet/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(WorksheetDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        numbering = self.request.GET.get('q', '')
        context['section_number'] = numbering.split('.')[0]
        context['module_number'] = numbering

        context['requirements'] = Specification.objects.filter(worksheet=pk)

        questions = WorksheetQuestion.objects.filter(worksheet=pk)
        context['questions'] = OrderedDict()
        for question in questions:
            context['questions'][question] = Answer.objects.filter(
                question=question)

        context['further_reading'] = FurtherReading.objects.filter(
            worksheet=pk)

        # Permissions
        context['user_can_edit'] = False
        if self.request.user in context[
            'worksheet'].section.project.lesson_managers.all():
            context['user_can_edit'] = True

        if self.request.user == context['worksheet'].section.project.owner:
            context['user_can_edit'] = True

        if self.request.user.is_staff:
            context['user_can_edit'] = True

        context['file_title'] = \
            context['worksheet'].section.name \
            + '-' + context['worksheet'].module
        context['file_title'] = context['file_title'].encode("utf8")
        return context


class WorksheetPrintView(WorksheetDetailView):
    """Based on the WorkSheet Detail View, this is one is used for
    downloading PDF module and sample test file.
    """

    template_name = 'worksheet/print.html'

    def render_to_response(self, context, **response_kwargs):
        numbering = self.request.GET.get('q', '')
        response = super(WorksheetPrintView, self).render_to_response(
            context, **response_kwargs)
        response.render()
        # return response
        pdf_response = HttpResponse(content_type='application/pdf')
        pdf_response['Content-Disposition'] = \
            'filename={}. {}'.format(numbering, context['file_title'])
        # Need to improve for URL outside of the dev env.
        html_object = HTML(
            string=response.content,
            base_url='file://',
        )
        html_object.write_pdf(pdf_response)
        return pdf_response


class WorksheetPDFZipView(WorksheetDetailView):
    """Based on the WorkSheet Detail View, this is one is used for printing.

    If you want to render as HTML for debugging, you can simply comment the
    render_to_response method or uncomment the first "return".
    """

    template_name = 'worksheet/print.html'

    def render_to_response(self, context, **response_kwargs):
        numbering = self.request.GET.get('q', '')
        response = super(WorksheetPDFZipView, self).render_to_response(
            context, **response_kwargs)
        response.render()
        # return response
        pdf_response = HttpResponse(content_type='application/pdf')
        pdf_response['Content-Disposition'] = \
            'attachment; filename={}'.format(context['file_title'])
        # Need to improve for URL outside of the dev env.
        html_object = HTML(
            string=response.content,
            base_url='file://',
        )
        html_object.write_pdf(pdf_response)

        filenames = []
        with open('/tmp/{}. {}.pdf'.format(
                numbering, context['file_title']), 'wb') as pdf:
            pdf.write(pdf_response.content)

        filenames.append(
            '/tmp/{}. {}.pdf'.format(numbering, context['file_title']))

        zip_subdir = '{}. {}'.format(numbering, context['file_title'])

        s = StringIO.StringIO()
        zf = zipfile.ZipFile(s, "w")

        for fpath in filenames:
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)

            zf.write(fpath, zip_path)

        if context['worksheet'].external_data:
            data_path = context['worksheet'].external_data.url
            zip_data_path = settings.MEDIA_ROOT + data_path[6:]
            zip_path = os.path.join(
                zip_subdir,
                '{}. {}.zip'.format(numbering, context['file_title']))
            zf.write(zip_data_path, zip_path)

        zf.close()

        zip_response = HttpResponse(
            s.getvalue(), content_type="application/x-zip-compressed")
        zip_response['Content-Disposition'] = \
            'attachment; filename={}. {}.zip'.format(
                numbering, context['file_title'])
        return zip_response


class WorksheetCreateView(LoginRequiredMixin, WorksheetMixin, CreateView):
    """Create view for Section."""

    context_object_name = 'worksheet'
    template_name = 'create.html'
    creation_label = _('Add worksheet')

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Version list page for the object's parent Project

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.pk,
            'section_slug': self.object.section.slug,
            'project_slug': self.object.section.project.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(WorksheetCreateView, self).get_form_kwargs()
        section_slug = self.kwargs['section_slug']
        kwargs['section'] = get_object_or_404(Section, slug=section_slug)
        return kwargs


class WorksheetUpdateView(LoginRequiredMixin, WorksheetMixin, UpdateView):
    """Update view for worksheet."""

    context_object_name = 'worksheet'
    template_name = 'update.html'
    update_label = _('Update worksheet')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(WorksheetUpdateView, self).get_form_kwargs()
        slug = self.kwargs.get('section_slug', None)
        kwargs['section'] = get_object_or_404(Section, slug=slug)
        return kwargs

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the section detail (worksheet list) page.

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.pk,
            'project_slug': self.object.section.project.slug,
            'section_slug': self.object.section.slug,
        })


class WorksheetDeleteView(
        LoginRequiredMixin,
        WorksheetMixin,
        DeleteView):
    """Delete view for worksheet."""

    context_object_name = 'worksheet'
    template_name = 'worksheet/delete.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the section detail (worksheet list) page
        for the object's parent Project.

        :returns: URL
        :rtype: HttpResponse
        """
        url = '{url}#{anchor}'.format(
            url=reverse(
                'section-list',
                kwargs={'project_slug': self.object.section.project.slug}),
            anchor=self.object.section.slug
        )
        return url


class WorksheetOrderView(LoginRequiredMixin, WorksheetMixin, ListView):
    """List view to order worksheet."""
    context_object_name = 'worksheets'
    template_name = 'worksheet/order.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(WorksheetOrderView, self).get_context_data(**kwargs)
        section_slug = self.kwargs.get('section_slug', None)
        context['section'] = Section.objects.get(slug=section_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved
            Categories.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        section_slug = self.kwargs.get('section_slug', None)
        section = get_object_or_404(Section, slug=section_slug)
        queryset = Worksheet.objects.filter(section=section)
        return queryset


class WorksheetOrderSubmitView(LoginRequiredMixin, WorksheetMixin, UpdateView):
    """Update order view for Worksheet."""

    def post(self, request, *args, **kwargs):
        """Post the project_slug from the URL and define the Project

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        :raises: Http404
        """
        section = Section.objects.get(slug=kwargs.get('section_slug'))
        worksheets = Worksheet.objects.filter(section=section)
        return re_order_features(request, worksheets)


class WorksheetModuleQuestionAnswers(WorksheetMixin,
                                     DetailView):
    """Show correct answers to module questions.

    :param request: HttpRequest object
    :type request: HttpRequest
    """
    context_object_name = 'worksheets'
    template_name = 'worksheet/question_answers.html'

    def get_context_data(self, **kwargs):
        """Create context for use in the templates."""

        context = super(WorksheetModuleQuestionAnswers,
                        self).get_context_data(**kwargs)
        project_slug = self.kwargs.get('project_slug', None)
        section_slug = self.kwargs.get('section_slug', None)
        project = get_object_or_404(Project, slug=project_slug)

        context['sections'] = Section.objects.filter(project=project,
                                                     slug=section_slug)
        for section in context['sections']:
            query_set = Worksheet.objects.filter(section=section)
            context['worksheets'] = []

            for worksheet in query_set:
                worksheet_json = {'worksheet': worksheet,
                                  'question_answers': []
                                  }

                worksheet_questions = WorksheetQuestion.objects.filter(
                        worksheet=worksheet.pk)

                for question in worksheet_questions:
                    question_json = {'question': question,
                                     'answer': []
                                     }
                    answers = Answer.objects.filter(question=question)

                    for answer in answers:
                        question_json['answer'].append(answer)
                    worksheet_json['question_answers'].append(question_json)
                context['worksheets'].append(worksheet_json)
        return context


def download_multiple_worksheet(request, **kwargs):
    """Download pdf and sample zip file from multiple worksheets."""

    project_slug = kwargs.pop('project_slug')
    project = Project.objects.get(slug=project_slug)
    worksheets_obj = request.GET.get('worksheet')
    worksheets = json.loads(worksheets_obj)

    def get_context_data(pk):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = {}
        context['worksheet'] = Worksheet.objects.get(pk=pk)
        context['requirements'] = Specification.objects.filter(worksheet=pk)

        questions = WorksheetQuestion.objects.filter(worksheet=pk)
        context['questions'] = OrderedDict()
        for question in questions:
            context['questions'][question] = Answer.objects.filter(
                question=question)

        context['further_reading'] = FurtherReading.objects.filter(
            worksheet=pk)

        context['file_title'] = \
            context['worksheet'].section.name \
            + '_' + context['worksheet'].title
        context['file_title'] = context['file_title'].encode("utf8")
        return context

    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")

    for pk in worksheets:
        numbering = worksheets[pk]
        pk = int(pk)
        worksheet = Worksheet.objects.get(pk=pk)
        pdf_title = '{}. {}'.format(numbering, worksheet.module.encode("utf8"))
        context = get_context_data(pk)
        context['section_number'] = numbering.split('.')[0]
        context['module_number'] = numbering
        response = render_to_response('worksheet/print.html', context=context)

        pdf_response = HttpResponse(content_type='application/pdf')
        pdf_response['Content-Disposition'] = \
            'attachment; filename={}'.format(pdf_title)

        html_object = HTML(
            string=response.content,
            base_url='file://',
        )
        html_object.write_pdf(pdf_response)

        with open('/tmp/{}.pdf'.format(pdf_title), 'wb') as pdf:
            pdf.write(pdf_response.content)

        fpath = '/tmp/{}.pdf'.format(pdf_title)

        dir_number = numbering.split('.')[0]
        zip_subdir = '{}. {}'.format(dir_number, worksheet.section.name)

        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        zf.write(fpath, zip_path)

        if worksheet.external_data:
            data_path = worksheet.external_data.url
            zip_data_path = settings.MEDIA_ROOT + data_path[6:]
            zip_path = os.path.join(zip_subdir, pdf_title + '.zip')
            zf.write(zip_data_path, zip_path)

    zf.close()

    zip_response = HttpResponse(
        s.getvalue(), content_type="application/x-zip-compressed")
    zip_response['Content-Disposition'] = \
        'attachment; filename={}-worksheet.zip'.format(
            project.name.encode('utf8'))
    return zip_response
