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
from models import Category, Version, Entry


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('project', 'name', 'sort_number')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                'Category details',
                Field('project', css_class="form-control"),
                Field('name', css_class="form-control"),
                Field('sort_number', css_class="form-control"),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))


class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = (
            'project',
            'name',
            'description',
            'image_file'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                'Version details',
                Field('project', css_class="form-control"),
                Field('name', css_class="form-control"),
                Field('description', css_class="form-control"),
                Field('image_file', css_class="form-control"),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(VersionForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(VersionForm, self).save(commit=False)
        instance.author = self.user
        instance.save()
        return instance


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = (
            'version', 'category', 'title', 'description',
            'image_file', 'image_credits'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                'Entry details',
                Field('version', css_class="form-control"),
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
        # Filter the category list when editing so it shows only relevant ones
        if self.instance.id is not None:
            self.fields['category'].queryset = Category.objects.filter(
                project=self.instance.version.project)

    def save(self, commit=True):
        instance = super(EntryForm, self).save(commit=False)
        instance.author = self.user
        instance.save()
        return instance
