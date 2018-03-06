# coding=utf-8
"""Mixin for lesson app."""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import override, get_language


class TranslationMixin(models.Model):
    """Translation mixin for managing translation."""

    last_update = models.DateTimeField(
        help_text=_('Time stamp when the last worksheet updated.'),
        blank=True,
        null=True
    )

    @property
    def is_translation_up_to_date(self):
        """Property to show if the translated version is up to date or not."""
        # Always up to date if the language is en.
        if get_language() == 'en':
            return True
        with override('en'):
            last_update_en = self.last_update
        # One of the last update is None, then translation is not up to date.
        if last_update_en is None or self.last_update is None:
            return False
        # Last update is older than English one --> no up to date.
        if self.last_update <= last_update_en:
            return False
        return True

    class Meta:
        abstract = True
