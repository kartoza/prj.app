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

from models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating projects."""

    class Meta:
        """Meta class."""
        model = Project
        fields = (
            'name',
            'image_file',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
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

    def save(self, commit=True):
        instance = super(ProjectForm, self).save(commit=False)
        instance.owner = self.user
        instance.save()
        return instance
