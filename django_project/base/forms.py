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

from models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating projects."""

    class Meta:
        """Meta class."""
        model = Project

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                'Project details',
                Field('name', css_class="form-control"),
                Field('image_file', css_class="form-control"),
                css_id='project-form')
            )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))
