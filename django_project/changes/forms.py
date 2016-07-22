# coding=utf-8
from django import forms
from django.core.validators import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from models import (
    Category,
    Version,
    Entry,
    Sponsor,
    SponsorshipPeriod,
    SponsorshipLevel
)


class CategoryForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = Category
        fields = ('name', 'sort_number')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.project = kwargs.pop('project')
        form_title = 'New Category in %s' % self.project.name
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('sort_number', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CategoryForm, self).save(commit=False)
        instance.project = self.project
        instance.save()
        return instance

    def clean(self):
        cleaned_data = self.cleaned_data

        try:
            Category.objects.get(name=cleaned_data['name'], project=self.project)
        except Category.DoesNotExist:
            pass
        else:
            raise ValidationError(
                'Category with this name already exists for this project'
            )

        return cleaned_data


class VersionForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = Version
        fields = (
            'name',
            'description',
            'image_file',
            'release_date'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'New Version for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('description', css_class='form-control'),
                Field('image_file', css_class='form-control'),

                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(VersionForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(VersionForm, self).save(commit=False)
        instance.author = self.user
        instance.project = self.project
        instance.approved = False
        instance.save()
        return instance


class EntryForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = Entry
        fields = (
            'category', 'title', 'description',
            'image_file', 'image_credits', 'video',
            'funded_by', 'funder_url', 'developed_by',
            'developer_url'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.version = kwargs.pop('version')
        self.project = kwargs.pop('project')
        form_title = 'New Entry in %s %s' % (
            self.project.name,
            self.version.name
        )
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('category', css_class='form-control'),
                Field('title', css_class='form-control'),
                Field('description', css_class='form-control'),
                Field('image_file', css_class='form-control'),
                Field('image_credits', css_class='form-control'),
                Field('video', css_class='form-control'),
                Field('funded_by', css_class='form-control'),
                Field('funder_url', css_class='form-control'),
                Field('developed_by', css_class='form-control'),
                Field('developer_url', css_class='form-control'),
                css_id='entry-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(EntryForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['title'].label = 'Feature Title'
        # Filter the category list when editing so it shows only relevant ones
        self.fields['category'].queryset = Category.objects.filter(
            project=self.project).order_by('name')

    def save(self, commit=True):
        instance = super(EntryForm, self).save(commit=False)
        instance.author = self.user
        instance.version = self.version
        instance.approved = False
        instance.save()
        return instance


class SponsorForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = Sponsor
        fields = (
            'name',
            'address',
            'country',
            'sponsor_url',
            'contact_person',
            'sponsor_email',
            'agreement',
            'logo'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'New Sponsor for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('address', css_class='form-control'),
                Field('country', css_class='form-control'),
                Field('sponsor_url', css_class='form-control'),
                Field('contact_person', css_class='form-control'),
                Field('sponsor_email', css_class='form-control'),
                Field('agreement', css_class='form-control'),
                Field('logo', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(SponsorForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(SponsorForm, self).save(commit=False)
        instance.author = self.user
        instance.project = self.project
        instance.approved = False
        instance.save()
        return instance


class SponsorshipLevelForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = SponsorshipLevel
        fields = (
            'name',
            'value',
            'currency',
            'logo'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'Sponsorship Level Form for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('value', css_class='form-control'),
                Field('currency', css_class='form-control'),
                Field('logo', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(SponsorshipLevelForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(SponsorshipLevelForm, self).save(commit=False)
        instance.author = self.user
        instance.project = self.project
        instance.save()
        return instance


class SponsorshipPeriodForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = SponsorshipPeriod
        fields = (
            'sponsor',
            'sponsorship_level',
            'start_date',
            'end_date'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'Sponsorship Period Form for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('sponsor', css_class='form-control'),
                Field('sponsorship_level', css_class='form-control'),
                Field('start_date', css_class='form-control'),
                Field('end_date', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(SponsorshipPeriodForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(SponsorshipPeriodForm, self).save(commit=False)
        instance.author = self.user
        instance.project = self.project
        instance.save()
        return instance
