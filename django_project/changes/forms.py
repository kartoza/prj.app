import logging
logger = logging.getLogger(__name__)
import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
     Layout,
     Fieldset,
     Submit,
     Div,
     HTML,
     Field,
     Button
)

from models import Entry


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                'Entry details',
                Field('category', css_class="form-control"),
                Field('title', css_class="form-control"),
                Field('description', css_class="form-control"),
                Field('image_file', css_class="form-control"),
                Field('image_credits', css_class="form-control"),
                css_id='entry-form')
            )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(EntryForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))
