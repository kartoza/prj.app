__author__ = 'rischan'

import os
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from audited_models.models import AuditedModel


class SponsorshipLevel(AuditedModel):
    """A sponsor model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text='Name of sponsorship level.',
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    logo = models.ImageField(
        help_text=(
            'An image of sponsorship level logo e.g. a bronze medal.'
            'Most browsers support dragging the image directly on to the '
            '"Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=False)

    def __unicode__(self):
        return '%s' % (self.name)
