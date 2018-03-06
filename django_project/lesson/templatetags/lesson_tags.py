# coding=utf-8
"""Custom tags for lesson app."""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='is_translation_up_to_date')
def is_translation_up_to_date(value):
    if not value.is_translation_up_to_date:
        return mark_safe(
            '<span title="Translation is outdated"><sup>&#x2757;</sup></span>')
    else:
        return mark_safe('')
