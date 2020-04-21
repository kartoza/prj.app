# coding=utf-8
import re
from django.core.validators import RegexValidator
from django.db.models.fields import SlugField
from django.forms.fields import SlugField as SlugFieldForm


slug_re = re.compile(r'^[-a-zA-Z0-9_.]+\Z')
custom_validate_slug = RegexValidator(
        slug_re,
        u"Enter a valid 'slug' consisting of letters, numbers, underscores, "
        u"dots or hyphens.",
        'invalid')


class CustomFormSlugField(SlugFieldForm):
    """A custom slugfield form where dots are allowed in the slug."""

    default_validators = [custom_validate_slug]
    default_error_messages = {
        'invalid': u"Enter a valid 'slug' consisting of letters, numbers, "
                   u"underscores, dots or hyphens.",
    }


class CustomSlugField(SlugField):
    """A custom slugfield where dots are allowed in the slug."""

    default_validators = [custom_validate_slug]
    default_error_messages = {
        'invalid': u"Enter a valid 'slug' consisting of letters, numbers, "
                   u"underscores, dots or hyphens.",
    }

    def formfield(self, **kwargs):
        defaults = {'form_class': CustomFormSlugField}
        defaults.update(kwargs)
        return super(SlugField, self).formfield(**defaults)
