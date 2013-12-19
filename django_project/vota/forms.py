import logging
import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Div,
    Submit,
    Field,
)
from vota.models import Vote, Committee, Ballot

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


class CreateCommitteeForm(forms.ModelForm):
    class Meta:
        model = Committee
        fields = (
            'name',
            'description',
            'sort_number',
            'quorum_setting',
            'project',
            'users'
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Field('name', css_class="form-control"),
            Field('description', css_class="form-control"),
            Field('sort_number', css_class="form-control"),
            Field('quorum_setting', css_class="form-control"),
            Field('project', css_class="form-control"),
            Field('users', css_class="form-control"),
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'committee-form'
        super(CreateCommitteeForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))


class BallotCreateForm(forms.ModelForm):
    class Meta:
        model = Ballot
        fields = (
            'committee',
            'name',
            'summary',
            'description',
            'open_from',
            'closes',
            'private'
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Field('committee', css_class="form-control"),
            Field('name', css_class="form-control"),
            Field('summary', css_class="form-control"),
            Field('description', css_class="form-control"),
            Field('open_from', css_class="form-control"),
            Field('closes', css_class="form-control"),
            Field('private', css_class="form-control"),
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'committee-form'
        super(BallotCreateForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))
