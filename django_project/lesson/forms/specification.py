# coding=utf-8
"""Section forms."""

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Field,
    Submit,
)

from modeltranslation.forms import TranslationModelForm
from lesson.models.specification import Specification


class SpecificationForm(TranslationModelForm):
    """Form for creating specification"""

    class Meta:
        model = Specification
        fields = (
            'title',
            'value',
            'notes'
        )

    def __init__(self, *args, **kwargs):
        self.worksheet = kwargs.pop('worksheet')
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                _('Specification details'),
                Field('title', css_class='form_control'),
                Field('value', css_class='form_control'),
                Field('notes', css_class='form_control'),
                css_id='project-form'
            )
        )

        self.helper.layout = layout
        self.helper.html5_required = False

        super(SpecificationForm, self).__init__(*args, **kwargs)

        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(SpecificationForm, self).save(commit=False)
        instance.worksheet = self.worksheet
        instance.save()
        return instance
