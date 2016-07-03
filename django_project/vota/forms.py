import logging
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Div,
    Submit,
    Field,
    Fieldset
)
from vota.models import Vote, Committee, Ballot

logger = logging.getLogger(__name__)


class VoteForm(forms.ModelForm):
    # noinspection PyClassicStyleClass
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
                Submit('submit', 'Submit', css_class='btn-sm'),
                css_class='form-group col-md-11 col-md-offset-1 margin-top'
            )
        )
        self.fields['choice'].widget = forms.RadioSelect()
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_class = 'form-inline col-md-10 col-md-offset-1'
        self.helper.form_id = 'vote-form'


class CreateCommitteeForm(forms.ModelForm):
    # noinspection PyClassicStyleClass
    class Meta:
        model = Committee
        fields = (
            'name',
            'description',
            'chair',
            'sort_number',
            'quorum_setting',
            'users',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'New Team for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class="form-control"),
                Field('description', css_class="form-control"),
                Field('chair', css_class="form-control"),
                Field('sort_number', css_class="form-control"),
                Field('quorum_setting', css_class="form-control"),
                Field('users', css_class="form-control"),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'committee-form'
        super(CreateCommitteeForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['chair'].queryset = self.fields['chair'].queryset \
            .order_by('username')
        self.fields['users'].queryset = self.fields['users'].queryset\
            .order_by('username')

    def save(self, commit=True):
        form = super(CreateCommitteeForm, self)
        instance = form.save(commit=False)
        instance.project = self.project
        instance.save()
        form.save()
        return instance


class BallotCreateForm(forms.ModelForm):
    # noinspection PyClassicStyleClass
    class Meta:
        model = Ballot
        fields = (
            'name',
            'summary',
            'description',
            'open_from',
            'closes',
            'private',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.committee = kwargs.pop('committee')
        form_title = 'New Ballot for %s' % self.committee.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class="form-control"),
                Field('summary', css_class="form-control"),
                Field('description', css_class="form-control"),
                Field('open_from', css_class="form-control"),
                Field('closes', css_class="form-control"),
                Field('private', css_class="form-control"),
            )
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
        instance.committee = self.committee
        instance.save()
        return instance
