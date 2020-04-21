# coding=utf-8
"""Answer views."""

from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from lesson.forms.answer import AnswerForm
from lesson.models.answer import Answer
from lesson.models.worksheet_question import WorksheetQuestion


class AnswerMixin(object):
    """Mixin class to provide standard settings for Answer."""

    model = Answer
    form_class = AnswerForm


class AnswerCreateView(
    LoginRequiredMixin, AnswerMixin, CreateView):
    """Create view for Answer."""

    context_object_name = 'answer'
    template_name = 'create.html'
    creation_label = _('Add answer')

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Version list page for the object's parent Worksheet

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.question.worksheet.pk,
            'section_slug': self.object.question.worksheet.section.slug,
            'project_slug': self.object.question.worksheet.section.project.slug
        })

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype dict
        """
        kwargs = super(AnswerCreateView, self).get_form_kwargs()
        pk = self.kwargs['question_pk']
        kwargs['question'] = get_object_or_404(WorksheetQuestion, pk=pk)
        return kwargs


# noinspection PyAttributeOutsideInit
class AnswerDeleteView(
        LoginRequiredMixin,
        AnswerMixin,
        DeleteView):
    """Delete view for Answer."""

    context_object_name = 'answer'
    template_name = 'answer/delete.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful deletion  of the object, the User will be redirected
        to the Certifying Organisation list page
        for the object's parent Worksheet.

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.question.worksheet.pk,
            'section_slug': self.object.question.worksheet.section.slug,
            'project_slug': self.object.question.worksheet.section.project.slug
        })


# noinspection PyAttributeOutsideInit
class AnswerUpdateView(
        LoginRequiredMixin,
        AnswerMixin,
        UpdateView):
    """Update view for Answer."""

    context_object_name = 'answer'
    template_name = 'update.html'
    update_label = _('Update answer')

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """
        kwargs = super(AnswerUpdateView, self).get_form_kwargs()
        answer = get_object_or_404(Answer, pk=kwargs['instance'].pk)
        kwargs['question'] = answer.question
        return kwargs

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the User will be redirected to
        the specification list page for the object's parent Worksheet.

        :returns: URL
        :rtype: HttpResponse
        """
        return reverse('worksheet-detail', kwargs={
            'pk': self.object.question.worksheet.pk,
            'section_slug': self.object.question.worksheet.section.slug,
            'project_slug': self.object.question.worksheet.section.project.slug
        })
