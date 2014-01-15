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
        fields = ('name', 'sort_number')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.project = kwargs.pop('project')
        form_title = 'New Category in %s' % self.project.name
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class="form-control"),
                Field('sort_number', css_class="form-control"),
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


class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = (
            'name',
            'description',
            'image_file'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'New Version for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
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
        instance.project = self.project
        instance.save()
        return instance


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = (
            'category', 'title', 'description',
            'image_file', 'image_credits'
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
        if not self.instance.id:
            self.fields['category'].queryset = Category.objects.filter(
                project=self.project).order_by('name')

    def save(self, commit=True):
        instance = super(EntryForm, self).save(commit=False)
        instance.author = self.user
        instance.version = self.version
        if self.user.is_staff:
            instance.approved = True
        instance.save()
        return instance
