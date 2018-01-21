# coding=utf-8
"""Answer form."""

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Field,
    Submit,
)

from modeltranslation.forms import TranslationModelForm
from lesson.models.answer import Answer


class AnswerForm(TranslationModelForm):
    """Form for creating answer."""

    class Meta:
        model = Answer
        fields = (
            'answer',
            'answer_explanation',
            'is_correct'
        )

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                _('Answer details'),
                Field('answer', css_class='form_control'),
                Field('answer_explanation', css_class='form_control'),
                Field('is_correct', css_class='form_control'),
                css_id='project-form'
            )
        )

        self.helper.layout = layout
        self.helper.html5_required = False

        super(AnswerForm, self).__init__(*args, **kwargs)

        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(AnswerForm, self).save(commit=False)
        instance.question = self.question
        instance.save()
        return instance
