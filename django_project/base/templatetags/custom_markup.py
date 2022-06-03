import markdown
from django import template
from django.contrib.staticfiles import finders
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text as force_unicode
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='base_markdown', is_safe=True)
@stringfilter
def base_markdown(value):
    extensions = ["nl2br", "markdown.extensions.tables", "fenced_code"]
    html_output = markdown.markdown(
        force_unicode(value),
        extensions=extensions,
        safe_mode=True,
        enable_attributes=False)
    html_output = html_output.replace(
        '<table>', '<table class="table table-striped table-bordered"')
    return mark_safe(html_output)


@register.filter(name='is_gif', is_safe=True)
@stringfilter
def is_gif(value):
    return value[-4:] == '.gif'


@register.filter
def local_static_filepath(value):
    """It gives the local filepath of a static file.

    Inspired by:
    https://stackoverflow.com/questions/9391167/django-how-to-get-a-static-
    files-filepath-in-a-development-environment

    :param value: The name of the static file to look for.

    :return: The local file path.
    """
    return finders.find(value)


@register.filter
def to_char(value):
    """Return a letter according to the number given.

    Eg 1 is returning "a".
    """
    return chr(96 + value)


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


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
