# coding=utf-8
"""Further reading views."""

from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
)
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from lesson.models.further_reading import FurtherReading
from lesson.models.worksheet import Worksheet
from lesson.forms.further_reading import FurtherReadingForm


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
