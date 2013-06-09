import logging
logger = logging.getLogger(__name__)
import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
     Layout,
     Submit,
     Div,
     HTML,
     Field,
     Button
)
from crispy_forms.bootstrap import (
     FormActions,
     Tab,
     TabHolder
)
from models import Entry


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.html5_required = False
        super(EntryForm, self).__init__(*args, **kwargs)

