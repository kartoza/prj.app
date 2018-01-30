# coding=utf-8
"""Further reading form."""

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Field,
    Submit,
)

from modeltranslation.forms import TranslationModelForm
from lesson.models.further_reading import FurtherReading


class FurtherReadingForm(TranslationModelForm):
    """Form for creating further reading item."""

    class Meta:
        model = FurtherReading
        fields = (
            'text',
            'link',
        )

    def __init__(self, *args, **kwargs):
        self.worksheet = kwargs.pop('worksheet')
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                _('Worksheet {}: further more item details').format(
                    self.worksheet),
                Field('text', css_class='form_control'),
                Field('link', css_class='form_control'),
                css_id='project-form'
            )
        )

        self.helper.layout = layout
        self.helper.html5_required = False

        super(FurtherReadingForm, self).__init__(*args, **kwargs)

        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(FurtherReadingForm, self).save(commit=False)
        instance.worksheet = self.worksheet
        instance.save()
        return instance
