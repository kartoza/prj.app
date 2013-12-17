import logging
import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Div,
    Submit,
    Field,
)
from vota.models import Vote

logger = logging.getLogger(__name__)


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = (
            'positive',
            'abstain',
            'negative'
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Field('positive', template='checkbox-field.html',
                  css_class='vote-checkbox'),
            Field('abstain', template='checkbox-field.html',
                  css_class='vote-checkbox'),
            Field('negative', template='checkbox-field.html',
                  css_class='vote-checkbox'),
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_class = 'form-inline'
        self.helper.form_id = 'vote-form'
        super(VoteForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))
