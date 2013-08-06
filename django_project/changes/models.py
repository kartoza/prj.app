import os
import logging
logger = logging.getLogger(__name__)
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from audited_models.models import AuditedModel


class Project(AuditedModel):
    """A project model e.g. QGIS, InaSAFE etc."""
    name = models.CharField(
        help_text='Name of this project.',
        max_length=255,
        null=False,
        blank=False,
        unique=True)

    image_file = models.ImageField(
        help_text='A logo image for this project.',
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=True)

    approved = models.BooleanField(
        help_text='Whether this project has been approved for use yet.'
    )

    def __unicode__(self):
        return u'%s' % self.name


class Version(AuditedModel):
    """A version model that the changelog is associated with.."""
    name = models.CharField(
        help_text='Name of this release e.g. 1.0.1.',
        max_length=255,
        null=False,
        blank=False,
        unique=False)

    approved = models.BooleanField(
        help_text=(
            'Whether this version has been approved for use by the '
            'project owner.')
    )

    project = models.ForeignKey(Project)

    class Meta:
        """Meta options for the version class."""
        unique_together = ('name', 'project')

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)


class Category(AuditedModel):
    """A category model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text='Name of this category.',
        max_length=255,
        null=False,
        blank=False,
        unique=True)

    approved = models.BooleanField(
        help_text=(
            'Whether this version has been approved for use by the '
            'project owner.')
    )

    project = models.ForeignKey(Project)


    class Meta:
        """Meta options for the category class."""
        unique_together = ('name', 'project')

    def __unicode__(self):
        return u'%s' % self.name


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
            'project owner.')
    )

    version = models.ForeignKey(Version)
    category = models.ForeignKey(Category)

    class Meta:
        """Meta options for the version class."""
        unique_together = ('title', 'version', 'category')

    def __unicode__(self):
        return u'%s' % self.title
