# coding=utf-8
"""Tools for Certification app."""


def check_slug(queryset, slug):
    """
    This function checks slug within a model and return a new incremented slug.

    """

    registered_slug = queryset.values_list('slug', flat=True)
    new_slug = slug
    if slug in registered_slug:
        match_slug = [s for s in registered_slug if slug in s]
        num = len(match_slug)
        new_slug = str(num) + '-' + slug

    return new_slug
