# coding=utf-8
"""Question views."""

import json

from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from base.models.project import Project
from lesson.forms.question import QuestionForm
from lesson.models.section import Section
from lesson.models.worksheet_question import WorksheetQuestion
from lesson.models.worksheet import Worksheet


class QuestionMixin(object):
    """Mixin class to provide standard settings for Question."""

    model = WorksheetQuestion
    form_class = QuestionForm


class QuestionCreateView(
    LoginRequiredMixin, QuestionMixin, CreateView):
    """Create view for Question."""

    context_object_name = 'question'
    template_name = 'specification/create.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
            QuestionCreateView, self).get_context_data(**kwargs)
        context['question'] = WorksheetQuestion.objects.filter(
            worksheet=self.worksheet)
        context['worksheet'] = self.worksheet
        return context

    def get_success_url(self):
        """Define the redirect URL

        After successful creation of the object, the User will be redirected
        to the unapproved Version list page for the object's parent Worksheet

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
        kwargs = super(QuestionCreateView, self).get_form_kwargs()
        self.worksheet_slug = self.kwargs.get('worksheet_slug', None)
        self.worksheet = Worksheet.objects.get(slug=self.worksheet_slug)
        kwargs.update({
            'worksheet': self.worksheet
        })
        return kwargs

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""
        try:
            result = super(QuestionCreateView, self).form_valid(form)
            return result
        except IntegrityError:
            raise ValidationError(
                'ERROR: Question by this name already exists!')


# noinspection PyAttributeOutsideInit
class QuestionDeleteView(
        LoginRequiredMixin,
        QuestionMixin,
        DeleteView):
    """Delete view for Question."""

    context_object_name = 'question'
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
            QuestionDeleteView, self).get(request, *args, **kwargs)

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
            QuestionDeleteView, self).post(request, *args, **kwargs)

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
class QuestionUpdateView(
        LoginRequiredMixin,
        QuestionMixin,
        UpdateView):
    """Update view for Question."""

    context_object_name = 'question'
    template_name = 'question/update.html'

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            QuestionUpdateView, self).get_form_kwargs()
        self.worksheet_slug = self.kwargs.get('worksheet_slug', None)
        self.worksheet = Worksheet.objects.get(slug=self.worksheet_slug)
        kwargs.update({
            'worksheet': self.worksheet
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            QuestionUpdateView, self).get_context_data(**kwargs)
        context['question'] = self.get_queryset() \
            .filter(worksheet=self.worksheet)
        context['the_worksheet'] = self.worksheet
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show all approved
        worksheets which user created (staff gets all worksheets)
        :rtype: QuerySet
        """

        self.worksheet_slug = self.kwargs.get('worksheet_slug', None)
        self.worksheet = Worksheet.objects.get(slug=self.worksheet_slug)
        if self.request.user.is_staff:
            queryset = WorksheetQuestion.objects.all()
        else:
            queryset = WorksheetQuestion.objects.filter(
                Q(worksheet=self.worksheet) &
                (Q(worksheet__owner=self.request.user) |
                 Q(organisation_owners=self.request.user)))
        return queryset

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

    def form_valid(self, form):
        """Check that there is no referential integrity error when saving."""

        try:
            return super(
                QuestionUpdateView, self).form_valid(form)
        except IntegrityError:
            return ValidationError(
                'ERROR: Question by this name is already exists!')


class QuestionOrderView(
    QuestionMixin, StaffuserRequiredMixin, ListView):
    """List view to order questions"""
    context_object_name = 'questions'
    template_name = 'question/order.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """
        context = super(
            QuestionOrderView, self).get_context_data(**kwargs)
        context['num_question'] = context['questions'].count()
        project_slug = self.kwargs.get('project_slug', None)
        section_slug = self.kwargs.get('section_slug', None)
        worksheet_slug = self.kwargs.get('worksheet_slug', None)
        if project_slug and section_slug and worksheet_slug:
            context['project'] = Project.objects.get(slug=project_slug)
            context['section'] = Section.objects.get(slug=section_slug)
            context['worksheet'] = Worksheet.objects.get(
                slug=worksheet_slug)
        return context

    def get_queryset(self, queryset=None):
        """Get the queryset for this view.

        :returns: A queryset which is filtered to only show approved
            Categories.

        :param queryset: Optional queryset.
        :rtype: QuerySet
        :raises: Http404
        """
        if queryset is None:
            worksheet_slug = self.kwargs.get('worksheet_slug', None)
            if worksheet_slug:
                try:
                    worksheet = Worksheet.objects.get(slug=worksheet_slug)
                except Worksheet.DoesNotExist:
                    raise Http404(
                        'Sorry! The worksheet you are requesting a '
                        'question for could not be found or you do not '
                        'have permission to view the question.')
                queryset = WorksheetQuestion.objects.filter(
                    worksheet=worksheet).order_by('question_number')
                return queryset
            else:
                raise Http404(
                        'Sorry! We could not find the worksheet for '
                        'your question!')
        else:
            return queryset


class QuestionOrderSubmitView(
    LoginRequiredMixin, QuestionMixin, UpdateView):
    """Update order view for Question"""
    context_object_name = 'specification'

    def post(self, request, *args, **kwargs):
        """Post the worksheet_slug from the URL and define the Worksheet

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
        worksheet_slug = kwargs.get('worksheet_slug')
        worksheet = Worksheet.objects.get(slug=worksheet_slug)
        questions = WorksheetQuestion.objects.filter(worksheet=worksheet)
        specifications_json = request.body

        try:
            questions_request = json.loads(specifications_json)
        except ValueError:
            raise Http404(
                'Error json values'
            )

        for question_request in questions_request:
            question = questions.get(pk=question_request['id'])
            if question:
                question.question_number = question_request['sort_number']
                question.save()

        return HttpResponse('')
