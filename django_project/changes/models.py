import os
import logging
logger = logging.getLogger(__name__)
from django.conf.global_settings import MEDIA_ROOT

from django.db import models


class Entry(models.Model):

    title = models.CharField(
        help_text='Title for this change note.',
        max_length=255,
        null=False,
        blank=False,
        unique=True)

    description = models.TextField(
        null=True,
        blank=True,
        help_text='Describe the new feature. Markdown is supported.')

    slug = models.SlugField()

    image_file = models.ImageField(
        help_text='A image that is related to this visual changelog entry.',
        upload_to=os.path.join(MEDIA_ROOT, 'images'),
        blank=True)

    image_credits = models.CharField(
        help_text='Who should be credited for this image?',
        max_length=255,
        null=True,
        blank=True)

    def __unicode__(self):
        return u'%s' % self.title
