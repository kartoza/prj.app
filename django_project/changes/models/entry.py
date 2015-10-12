# coding=utf-8
"""Models for changelog entries."""
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import os
import logging
from core.settings.contrib import STOP_WORDS
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from audited_models.models import AuditedModel
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class ApprovedEntryManager(models.Manager):
    """Custom entry manager that shows only approved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedEntryManager, self).get_query_set().filter(
                approved=True)


class UnapprovedEntryManager(models.Manager):
    """Custom entry manager that shows only unapproved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            UnapprovedEntryManager, self).get_query_set().filter(
                approved=False)


class Entry(AuditedModel):
    """An entry is the basic unit of a changelog."""
    title = models.CharField(
        help_text='Feature title for this changelog entry.',
        max_length=255,
        null=False,
        blank=False,
        unique=True)

    description = models.TextField(
        null=True,
        blank=True,
        help_text='Describe the new feature. Markdown is supported.')

    image_file = models.ImageField(
        help_text=(
            'A image that is related to this visual changelog entry. '
            'Most browsers support dragging the image directly on to the '
            '"Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/entries'),
        blank=True)

    image_credits = models.CharField(
        help_text='Who should be credited for this image?',
        max_length=255,
        null=True,
        blank=True)

    video = EmbedVideoField(verbose_name='Youtube video',
                            help_text='Paste your youtube video link',
                            null=True,
                            blank=True)

    approved = models.BooleanField(
        help_text=(
            'Whether this entry has been approved for use by the '
            'project owner.'),
        default=False
    )
    author = models.ForeignKey(User)
    slug = models.SlugField()
    # noinspection PyUnresolvedReferences
    version = models.ForeignKey('Version')
    # noinspection PyUnresolvedReferences
    category = models.ForeignKey('Category')
    objects = models.Manager()
    approved_objects = ApprovedEntryManager()
    unapproved_objects = UnapprovedEntryManager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the version class."""
        unique_together = (
            ('title', 'version', 'category'),
            ('version', 'slug'),
        )
        app_label = 'changes'

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.title.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(Entry, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('entry-detail', kwargs={
            'slug': self.slug,
            'version_slug': self.version.slug,
            'project_slug': self.version.project.slug
        })
