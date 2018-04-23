# coding=utf-8

from django import template
from core.settings.utils import absolute_path

register = template.Library()

@register.simple_tag(takes_context=True)
def version_tag(context):
    """Reads current project release from the .version file."""
    version_file = absolute_path('.version')
    try:
        with open(version_file, 'r') as file:
            version = file.read()
            context['version'] = version
    except:
        context['version'] = 'Unknown'
    return context['version']