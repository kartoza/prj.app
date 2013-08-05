import os
import logging
logger = logging.getLogger(__name__)
from django.conf.global_settings import MEDIA_ROOT
from django.db import models


class Project(models.Model):
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

    def __unicode__(self):
        return u'%s' % self.name


class Version(models.Model):
    """A version model that the changelog is associated with.."""
    name = models.CharField(
        help_text='Name of this release e.g. 1.0.1.',
        max_length=255,
        null=False,
        blank=False,
        unique=False)

    project = models.ForeignKey(Project)

    class Meta:
        """Meta options for the version class."""
        unique_together = ('name', 'project')

    def __unicode__(self):
        return u'%s' % self.name


class Category(models.Model):
    """A category model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text='Name of this category.',
        max_length=255,
        null=False,
        blank=False,
        unique=True)

    project = models.ForeignKey(Project)


    class Meta:
        """Meta options for the category class."""
        unique_together = ('name', 'project')

    def __unicode__(self):
        return u'%s' % self.name


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

    image_file = models.ImageField(
        help_text='A image that is related to this visual changelog entry.',
        upload_to=os.path.join(MEDIA_ROOT, 'images'),
        blank=True)

    image_credits = models.CharField(
        help_text='Who should be credited for this image?',
        max_length=255,
        null=True,
        blank=True)

    category = models.ForeignKey(Version)

    class Meta:
        """Meta options for the version class."""
        unique_together = ('title', 'category')

    def __unicode__(self):
        return u'%s' % self.title
