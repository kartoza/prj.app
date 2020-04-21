# coding=utf-8
"""Custom tags for lesson app."""
from django import template
from django.utils.safestring import mark_safe
from core.settings.utils import absolute_path


register = template.Library()


@register.filter(name='is_translation_up_to_date')
def is_translation_up_to_date(value):
    if not value.is_translation_up_to_date:
        return mark_safe(
            '<span title="Translation is outdated"><sup>&#x2757;</sup></span>')
    else:
        return mark_safe('')


@register.simple_tag(takes_context=True)
def version_tag(context):
    """Reads current project release from the .version file."""
    version_file = absolute_path('.version')
    try:
        with open(version_file, 'r') as file:
            version = file.read()
            context['version'] = version
    except IOError:
        context['version'] = 'Unknown'
    return context['version']
