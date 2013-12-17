# coding=utf-8
"""Project model used by all apps."""
from django.utils.text import slugify
import os
import logging
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _
from audited_models.models import AuditedModel
from changes.models.version import Version

logger = logging.getLogger(__name__)


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


class PublicProjectManager(models.Manager):
    """Custom project manager that shows only public and approved projects."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            PublicProjectManager, self).get_query_set().filter(
                private=False).filter(approved=True)


class Project(AuditedModel):
    """A project model e.g. QGIS, InaSAFE etc."""
    name = models.CharField(
        help_text=_('Name of this project.'),
        max_length=255,
        null=False,
        blank=False,
        unique=True)

    description = models.CharField(
        help_text=_('A description for the project'),
        max_length=500,
        blank=True,
        null=True
    )

    image_file = models.ImageField(
        help_text=_('A logo image for this project. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=True
    )

    approved = models.BooleanField(
        help_text=_('Whether this project has been approved for use yet.'),
        default=False
    )

    private = models.BooleanField(
        help_text=_('Only visible to logged-in users?'),
        default=False
    )

    slug = models.SlugField(unique=True)
    objects = models.Manager()
    approved_objects = ApprovedProjectManager()
    unapproved_objects = UnapprovedProjectManager()
    public_objects = PublicProjectManager()

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
