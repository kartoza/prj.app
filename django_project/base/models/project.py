# coding=utf-8
"""Project model used by all apps."""
from django.utils.text import slugify
import os
import logging
logger = logging.getLogger(__name__)
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from audited_models.models import AuditedModel
from changes.models.version import Version


class ApprovedProjectManager(models.Manager):
    """Custom project manager that shows only approved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedProjectManager, self).get_query_set().filter(
                approved=True)


class UnapprovedProjectManager(models.Manager):
    """Custom project manager that shows only unapproved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            UnapprovedProjectManager, self).get_query_set().filter(
                approved=False)


class Project(AuditedModel):
    """A project model e.g. QGIS, InaSAFE etc."""
    name = models.CharField(
        help_text='Name of this project.',
        max_length=255,
        null=False,
        blank=False,
        unique=True)

    image_file = models.ImageField(
        help_text=('A logo image for this project. '
                   'Most browsers support dragging the image directly on to '
                   'the "Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=True)

    approved = models.BooleanField(
        help_text='Whether this project has been approved for use yet.',
        default=False
    )
    slug = models.SlugField(unique=True)
    objects = ApprovedProjectManager()
    all_objects = models.Manager()
    unapproved_objects = UnapprovedProjectManager()

    class Meta:
        """Meta class for project."""
        app_label = 'base'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name

    def versions(self):
        """Get all the versions for this project."""
        qs = Version.objects.filter(project=self).order_by('name')
        return qs
