# coding=utf-8
import datetime
import logging
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Field,
    Submit,
)
from models import(
    Project,
    ProjectScreenshot,
    Domain,
    Organisation
)
from django_project.base.models.stripe_sale import Sale
from certification.forms import CustomSelectMultipleWidget

logger = logging.getLogger(__name__)


class ProjectScreenshotForm(forms.ModelForm):
    """Form to input a screenshot linked to a project."""

    class Meta:
        model = ProjectScreenshot
        fields = ('screenshot',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.form_method = 'post'
        layout = Layout(
            Fieldset(
                'Screenshot',
                Field('screenshot', css_class="form-control"),
                Field('DELETE', css_class='input-small'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(ProjectScreenshotForm, self).__init__(*args, **kwargs)


class ProjectForm(forms.ModelForm):
    """Form for creating projects."""

    certification_manager = forms.ModelMultipleChoiceField(
        queryset=User.objects.order_by('username'),
        widget=CustomSelectMultipleWidget("user", is_stacked=False),
        required=False,
        help_text=_(
            'Managers of the certification app in this project. '
            'They will receive email notification about organisation and have'
            ' the same permissions as project owner in the certification app.')
    )

    changelog_manager = forms.ModelMultipleChoiceField(
        queryset=User.objects.order_by('username'),
        widget=CustomSelectMultipleWidget("user", is_stacked=False),
        required=False,
        help_text=_(
            'Managers of the changelog in this project. '
            'They will be allowed to approve changelog entries in the '
            'moderation queue.')
    )

    sponsorship_manager = forms.ModelMultipleChoiceField(
        queryset=User.objects.order_by('username'),
        widget=CustomSelectMultipleWidget("user", is_stacked=False),
        required=False,
        help_text=_(
            'Managers of the sponsorship in this project. '
            'They will be allowed to approve sponsorship entries in the '
            'moderation queue.')
    )

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class."""
        model = Project
        fields = (
            'name',
            'organisation',
            'image_file',
            'description',
            'project_url',
            'precis',
            'gitter_room',
            'signature',
            'changelog_manager',
            'sponsorship_manager',
            'certification_manager',
            'credit_cost',
            'certificate_credit',
            'sponsorship_programme',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.helper = FormHelper()
        self.helper.form_tag = False
        layout = Layout(
            Fieldset(
                'Project details',
                Field('name', css_class="form-control"),
                Field('organisation', css_class="form-control"),
                Field('image_file', css_class="form-control"),
                Field('description', css_class="form-control"),
                Field('project_url', css_class="form-control"),
                Field('precis', css_class="form-control"),
                Field('signature', css_class="form-control"),
                Field('changelog_manager', css_class="form-control"),
                Field('sponsorship_manager', css_class="form-control"),
                Field('certification_manager', css_class="form-control"),
                Field('credit_cost', css_class="form-control"),
                Field('certificate_credit', css_class="form-control"),
                Field('sponsorship_programme', css_class="form-control"),
                Field('gitter_room', css_class="form-control"),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['changelog_manager'].label_from_instance = \
            lambda obj: "%s <%s>" % (obj.get_full_name(), obj)
        self.fields['sponsorship_manager'].label_from_instance = \
            lambda obj: "%s <%s>" % (obj.get_full_name(), obj)
        self.fields['certification_manager'].label_from_instance = \
            lambda obj: "%s <%s>" % (obj.get_full_name(), obj)
        # self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(ProjectForm, self).save(commit=False)
        instance.owner = self.user
        instance.save()
        self.save_m2m()
        return instance


# Screenshot formset
ScreenshotFormset = \
    inlineformset_factory(
        Project,
        ProjectScreenshot,
        form=ProjectScreenshotForm,
        extra=5)


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        label='First Name (Optional)',
        required=False,
        widget=forms.TextInput(
            {
                "placeholder": _('First Name')
            })
    )

    last_name = forms.CharField(
        max_length=150,
        label='Last Name (Optional)',
        required=False,
        widget=forms.TextInput(
            {
                "placeholder": _('Last Name')
            })
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class RegisterDomainForm(forms.ModelForm):
    """Form to register a domain."""

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class."""
        model = Domain
        fields = (
            'domain',
            'role',
            'project',
            'organisation',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        form_title = 'Register a Domain'
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('domain', css_class='form-control'),
                Field('role', css_class='form-control'),
                Field('project', css_class='form-control'),
                Field('organisation', css_class='form-control'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(RegisterDomainForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(RegisterDomainForm, self).save(commit=False)
        instance.user = self.user
        instance.save()
        return instance


class OrganisationForm(forms.ModelForm):
    """Form to create an organisation that is associated to a project."""

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class."""
        model = Organisation
        fields = (
            'name',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        form_title = 'Create an Organisation'
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(OrganisationForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(OrganisationForm, self).save(commit=False)
        instance.owner = self.user
        instance.save()
        return instance


# stripe payment form
class CreditCardField(forms.IntegerField):
    def clean(self, value):
        """Check if given CC number is valid and one of thecard types we accept.
        """
        if value and (len(value) > 13 or len(value) < 16):
            # and (len(value) & lt; 13 or len(value) & gt; 16):
            raise forms.ValidationError("Please enter in a valid " + \
                                        "credit card number.")
        return super(CreditCardField, self).clean(value)


class CCExpWidget(forms.MultiWidget):
    """Widget containing two select boxes for selecting the month and year."""

    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]

    def format_output(self, rendered_widgets):
        html = u' / '.join(rendered_widgets)
        return u'<span style="white-space: nowrap;">%s</span>' % html


class CCExpField(forms.MultiValueField):
    EXP_MONTH = [(x, x) for x in xrange(1, 13)]
    EXP_YEAR = [(x, x) for x in xrange(datetime.date.today().year,
                            datetime.date.today().year + 15)]
    default_error_messages = {
        'invalid_month': u'Enter a valid month.',
        'invalid_year': u'Enter a valid year.',
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.ChoiceField(
                choices=self.EXP_MONTH,
                error_messages={'invalid': errors['invalid_month']}
            ),

            forms.ChoiceField(
                choices=self.EXP_YEAR,
                error_messages={'invalid': errors['invalid_year']}
            ),
        )

        super(CCExpField, self).__init__(fields, *args, **kwargs)
        self.widget = CCExpWidget(widgets=
                                  [fields[0].widget, fields[1].widget])

    def clean(self, value):
        exp = super(CCExpField, self).clean(value)
        if datetime.datetime.today() > exp:
            raise forms.ValidationError(
                "The expiration date you entered is in the past.")
        return exp

    def compress(self, data_list):
        if data_list:
            if data_list[1] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_year']
                raise forms.ValidationError(error)
            if data_list[0] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_month']
                raise forms.ValidationError(error)
            year = int(data_list[1])
            month = int(data_list[0])

            # find last day of the month
            now = datetime.datetime.now()
            one_day_in_future = datetime.timedelta(days=1)

            day = now + one_day_in_future

            return datetime.datetime.date(year, month, day)
        return None


class SalePaymentForm(forms.Form):
    number = CreditCardField(
        label=_("Card Number"),
        required=True
    )

    expiration = CCExpField(
        label=_("Expiration"),
        required=True
    )

    cvc = forms.IntegerField(
        label=_("CCV Number"),
        required=True,
        max_value=9999,
        widget=forms.TextInput(
            attrs={'size': '4'}
        )
    )

    def clean(self):
        """
        The clean method will effectively charge the card and create a new
        Sale instance. If it fails, it simply raises the error given from
        Stripe's library as a standard ValidationError for proper feedback.
        """

        cleaned = super(SalePaymentForm, self).clean()

        if not self.errors:
            number = self.cleaned_data["number"]
            exp_month = self.cleaned_data["expiration"].month
            exp_year = self.cleaned_data["expiration"].year
            cvc = self.cleaned_data["cvc"]

            sale = Sale()

            # Here we import a charge that we have customly
            # defined in the settings file
            success, instance = sale.charge(
                settings.STRIPE_CHARGE_AMOUNT,
                number,
                exp_month,
                exp_year,
                cvc
            )

            if not success:
                raise forms.ValidationError("Error: %s" % instance.message)
            else:
                instance.save()
                # we were successful! do whatever you will here...
                # perhaps you'd like to send an email...
                pass

        return cleaned