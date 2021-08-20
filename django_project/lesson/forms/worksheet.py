# coding=utf-8
"""Worksheet form."""

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Field,
    Submit,
)

from modeltranslation.forms import TranslationModelForm
from lesson.models.worksheet import Worksheet

from lesson.utilities import validate_zipfile


class WorksheetForm(TranslationModelForm):
    """Form for creating worksheet."""

    class Meta:
        model = Worksheet
        fields = (
            'module',
            'title',
            'summary_leader',
            'summary_text',
            'summary_image',
            'exercise_goal',
            'exercise_task',
            'exercise_image',
            'requirement_header_name_first',
            'requirement_header_name_last',
            'more_about_title',
            'more_about_text',
            'more_about_image',
            'external_data',
            'youtube_link',
            'author_name',
            'author_link',
            'license',
            'summary_image_dimension',
            'exercise_image_dimension',
            'more_about_image_dimension',
            'funded_by',
            'funder_url',
            'published',
            #  checkbox for page break between content
            'page_break_before_exercise',
            'page_break_before_requirement_table',
            'page_break_before_exercise_image',
            'page_break_before_more_about',
            'page_break_before_question',
            'page_break_before_youtube_link',
            'page_break_before_further_reading',
        )

    def __init__(self, *args, **kwargs):
        self.section = kwargs.pop('section')
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                _('Section {}: worksheet details').format(self.section),
                Field('module', css_class='form_control'),
                Field('title', css_class='form_control'),
                Field('summary_leader', css_class='form_control'),
                Field('summary_text', css_class='form_control'),
                Field('summary_image', css_class='form_control'),
                Field('summary_image_dimension', css_class='form_control'),
                Field('exercise_goal', css_class='form_control'),
                Field('exercise_task', css_class='form_control'),
                Field('exercise_image', css_class='form_control'),
                Field('requirement_header_name_first',
                      css_class='form_control'),
                Field('requirement_header_name_last',
                      css_class='form_control'),
                Field('exercise_image_dimension', css_class='form_control'),
                Field('more_about_title', css_class='form_control'),
                Field('more_about_text', css_class='form_control'),
                Field('more_about_image', css_class='form_control'),
                Field('more_about_image_dimension', css_class='form_control'),
                Field('external_data', css_class='form_control'),
                Field('youtube_link', css_class='form_control'),
                Field('license', css_class='form_control'),
                Field('funded_by', css_class='form_control'),
                Field('funder_url', css_class='form_control'),
                Field('published', css_class='form_control'),
                Field('page_break_before_exercise', css_class='form_control'),
                Field('page_break_before_requirement_table',
                      css_class='form_control'),
                Field('page_break_before_exercise_image',
                      css_class='form_control'),
                Field('page_break_before_more_about',
                      css_class='form_control'),
                Field('page_break_before_question', css_class='form_control'),
                Field('page_break_before_youtube_link',
                      css_class='form_control'),
                Field('page_break_before_further_reading',
                      css_class='form_control'),
                css_id='project-form'
            )
        )

        self.helper.layout = layout
        self.helper.html5_required = False

        super(WorksheetForm, self).__init__(*args, **kwargs)

        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(WorksheetForm, self).save(commit=False)
        instance.section = self.section
        instance.save()
        return instance

    def clean_external_data(self):
        """validate the zipfile during uploading."""

        file = self.cleaned_data['external_data']
        if file and validate_zipfile(file):
            return file


class WorksheetUpdateForm(WorksheetForm):
    def __init__(self, *args, **kwargs):
        super(WorksheetUpdateForm, self).__init__(*args, **kwargs)
        # insert in the bottom of page
        self.helper.layout.insert(
            0, Field('section', css_class='form_control'))
        self.fields['section'].help_text = "Select to change the section."

    class Meta(WorksheetForm.Meta):
        fields = WorksheetForm.Meta.fields + ('section',)

    def save(self, commit=True):
        instance = super(WorksheetForm, self).save(commit=False)
        instance.save()
        return instance
