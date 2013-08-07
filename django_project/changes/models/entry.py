import os
import logging
logger = logging.getLogger(__name__)
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from audited_models.models import AuditedModel


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

    image_file = models.ImageField(
        help_text='A image that is related to this visual changelog entry.',
        upload_to=os.path.join(MEDIA_ROOT, 'images'),
        blank=True)

    image_credits = models.CharField(
        help_text='Who should be credited for this image?',
        max_length=255,
        null=True,
        blank=True)

    approved = models.BooleanField(
        help_text=(
            'Whether this entry has been approved for use by the '
            'project owner.'),
        default=False
    )

    version = models.ForeignKey('Version')
    category = models.ForeignKey('Category')

    objects = ApprovedEntryManager()
    all_objects = models.Manager()
    unapproved_objects = UnapprovedEntryManager()

    class Meta:
        """Meta options for the version class."""
        unique_together = ('title', 'version', 'category')
        app_label = 'changes'

    def __unicode__(self):
        return u'%s' % self.title
