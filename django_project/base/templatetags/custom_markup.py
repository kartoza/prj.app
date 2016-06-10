import markdown
import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='base_markdown', is_safe=True)
@stringfilter
def base_markdown(value):
    extensions = ["nl2br", ]

    return mark_safe(markdown.markdown(force_unicode(value),
                                       extensions,
                                       safe_mode=True,
                                       enable_attributes=False))


@register.filter(name='is_gif', is_safe=True)
@stringfilter
def is_gif(value):
    return bool(re.search('.gif', value))

