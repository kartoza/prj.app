"""License Model for lesson content"""

import os

from django.db import models
from django.conf.global_settings import MEDIA_ROOT
from django.utils.translation import ugettext_lazy as _

from model_utils import FieldTracker

from lesson.models.mixins import TranslationMixin


class License(TranslationMixin):
    tracker = FieldTracker()

    name = models.CharField(
        help_text=_('Name of license.'),
        blank=False,
        null=False,
        max_length=200,
    )

    description = models.TextField(
        help_text=_('Describe the license.'),
        blank=False,
        null=False,
    )

    url = models.URLField(
        help_text=_('Input the license URL.'),
        blank=False,
        null=False,
        max_length=200,
    )

    file = models.FileField(
        help_text=_('License content in the text format. Usually a txt file. '
                    'Most browsers support dragging the file directly '
                    'on to the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/license'),
        blank=False
    )

    class Meta:
        """Meta class for Section model."""

        app_label = 'lesson'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


from lesson.signals.license import *  # noqa
