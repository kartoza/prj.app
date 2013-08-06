import os
import logging
logger = logging.getLogger(__name__)
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from audited_models.models import AuditedModel


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
        help_text='A logo image for this project.',
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=True)

    approved = models.BooleanField(
        help_text='Whether this project has been approved for use yet.',
        default=False
    )

    objects = ApprovedProjectManager()
    all_objects = models.Manager()
    unapproved_objects = UnapprovedProjectManager()

    def __unicode__(self):
        return u'%s' % self.name

    def versions(self):
        """Get all the versions for this project."""
        qs = Version.objects.filter(project=self)
        return qs


class ApprovedVersionManager(models.Manager):
    """Custom version manager that shows only approved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedVersionManager, self).get_query_set().filter(
                approved=True)


class UnapprovedVersionManager(models.Manager):
    """Custom version manager that shows only unapproved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            UnapprovedVersionManager, self).get_query_set().filter(
                approved=False)


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
            'project owner.'),
        default=False)

    project = models.ForeignKey(Project)

    objects = ApprovedVersionManager()
    all_objects = models.Manager()
    unapproved_objects = UnapprovedVersionManager()

    class Meta:
        """Meta options for the version class."""
        unique_together = ('name', 'project')

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)


class ApprovedCategoryManager(models.Manager):
    """Custom category manager that shows only approved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedCategoryManager, self).get_query_set().filter(
                approved=True)


class UnapprovedCategoryManager(models.Manager):
    """Custom version manager that shows only unapproved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            UnapprovedCategoryManager, self).get_query_set().filter(
                approved=False)


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
            'project owner.'),
        default=False
    )

    project = models.ForeignKey(Project)

    objects = ApprovedCategoryManager()
    all_objects = models.Manager()
    unapproved_objects = UnapprovedCategoryManager()

    class Meta:
        """Meta options for the category class."""
        unique_together = ('name', 'project')

    def __unicode__(self):
        return u'%s' % self.name


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

    version = models.ForeignKey(Version)
    category = models.ForeignKey(Category)

    objects = ApprovedEntryManager()
    all_objects = models.Manager()
    unapproved_objects = UnapprovedEntryManager()

    class Meta:
        """Meta options for the version class."""
        unique_together = ('title', 'version', 'category')

    def __unicode__(self):
        return u'%s' % self.title
