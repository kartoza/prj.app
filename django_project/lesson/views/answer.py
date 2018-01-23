# coding=utf-8
"""Answer views."""

from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
)
from django.http import Http404
from django.core.exceptions import ValidationError
from django.db import IntegrityError

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
    template_name = 'answer/create.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
            AnswerCreateView, self).get_context_data(**kwargs)
        context['answer'] = Answer.objects.filter(
            question=self.question)
        context['question'] = self.question
        return context

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
        self.question_pk = self.kwargs.get('question_pk', None)
        self.question = WorksheetQuestion.objects.get(pk=self.question_pk)
        kwargs.update({
            'question': self.question
        })
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            result = super(AnswerCreateView, self).form_valid(form)
            return result
        except IntegrityError:
            raise ValidationError(
                'ERROR: Answer by this name already exists!')


# noinspection PyAttributeOutsideInit
class AnswerDeleteView(
        LoginRequiredMixin,
        AnswerMixin,
        DeleteView):
    """Delete view for Answer."""

    context_object_name = 'answer'
    template_name = 'question/delete.html'

    def get(self, request, *args, **kwargs):
        """Get the worksheet_slug from the URL and define the Worksheet.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.pk = self.kwargs.get('pk', None)
        return super(
            AnswerDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post the worksheet_slug from the URL and define the Worksheet.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: Unaltered request object
        :rtype: HttpResponse
        """
        self.pk = self.kwargs.get('pk', None)
        return super(
            AnswerDeleteView, self).post(request, *args, **kwargs)

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

    def get_queryset(self):
        """Get the queryset for this view.

        We need to filter the CertifyingOrganisation objects by
        Worksheet before passing to get_object() to ensure that we
        return the correct Certifying Organisation object.
        The requesting User must be authenticated.

        :returns: Certifying Organisation queryset filtered by Worksheet
        :rtype: QuerySet
        :raises: Http404
        """

        if not self.request.user.is_authenticated():
            raise Http404
        qs = WorksheetQuestion.objects.filter(pk=self.pk)
        return qs


# noinspection PyAttributeOutsideInit
class AnswerUpdateView(
        LoginRequiredMixin,
        AnswerMixin,
        UpdateView):
    """Update view for Answer."""

    context_object_name = 'answer'
    template_name = 'answer/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(AnswerUpdateView, self).get_form_kwargs()
        self.pk = self.kwargs.get('pk', None)
        self.answer = Answer.objects.get(pk=self.pk)
        kwargs.update({
            'question': self.answer.question
        })
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
