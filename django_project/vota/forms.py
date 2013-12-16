import logging
logger = logging.getLogger(__name__)
import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from vota.models import Vote


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                'Place Your Vote',
                Field('positive', css_class="form-control"),
                Field('abstain', css_class="form-control"),
                Field('negative', css_class="form-control"),
                css_id='vote-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(VoteForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))
