import markdown
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
    return value[-4:] == '.gif'


@register.inclusion_tag('button_span.html', takes_context=True)
def show_button_icon(context, value):

    context_icon = {
        'add': 'glyphicon glyphicon-asterisk',
        'update': 'glyphicon glyphicon-pencil',
        'delete': 'glyphicon glyphicon-minus',
        'back': 'glyphicon glyphicon-arrow-left'
    }

    return {
        'button_icon': context_icon[value]
    }


@register.filter
def columns(thelist, n):
    """
    Break a list into ``n`` columns, filling up each column to the maximum
    equal length possible. For example::
    """
    try:
        n = int(n)
        thelist = list(thelist)
    except (ValueError, TypeError):
        return [thelist]
    list_len = len(thelist)
    split = list_len // n
    if list_len % n != 0:
        split += 1
    return [thelist[i::split] for i in range(split)]
