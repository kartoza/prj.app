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
            'choice',
        )

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        layout = Layout(
            Field('choice', template='radio-select.html'),
            Div(
                Submit('submit', 'Submit'),
                css_class='form-group col-md-11 col-md-offset-1 margin-top'
            )
        )
        self.fields['choice'].widget = forms.RadioSelect()
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_class = 'form-inline col-md-10 col-md-offset-1'
        self.helper.form_id = 'vote-form'


class CreateCommitteeForm(forms.ModelForm):
    class Meta:
        model = Committee
        fields = (
            'name',
            'description',
            'sort_number',
            'quorum_setting',
            'project',
            'users',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
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

    def save(self, commit=True):
        instance = super(CreateCommitteeForm, self).save(commit=False)
        instance.chair = self.user
        instance.save()
        return instance


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
            'private',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
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

    def save(self, commit=True):
        instance = super(BallotCreateForm, self).save(commit=False)
        instance.proposer = self.user
        instance.save()
        return instance
