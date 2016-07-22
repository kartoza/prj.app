# coding=utf-8
"""Project model used by all apps."""
import os
import logging
import string
import re
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _
from changes.models.version import Version
from core.settings.contrib import STOP_WORDS
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from permission.models.project_collaborator import ProjectCollaborator
from permission.models.project_administrator import ProjectAdministrator

logger = logging.getLogger(__name__)


class ApprovedProjectManager(models.Manager):
    """Custom project manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            ApprovedProjectManager, self).get_queryset().filter(
            approved=True)


class UnapprovedProjectManager(models.Manager):
    """Custom project manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            UnapprovedProjectManager, self).get_queryset().filter(
            approved=False)


class PublicProjectManager(models.Manager):
    """Custom project manager that shows only public and approved projects."""

    def get_queryset(self):
        """Query set generator"""
        return super(
            PublicProjectManager, self).get_queryset().filter(
            private=False).filter(approved=True)


def validate_gitter_room_name(value):
    """Ensure user enter proper gitter room name

    :param value: string input
    :raises: ValidationError
    """
    invalid_chars = set(string.punctuation.replace('/', ''))
    pattern = re.compile('^(\w+\/\w+)$')
    if any(char in invalid_chars for char in value) \
            or not pattern.match(value):
        raise ValidationError(
            _('%(value)s is not proper gitter room name'),
            params={'value': value},
        )


class Project(models.Model):
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

    owner = models.ForeignKey(User)
    slug = models.SlugField(unique=True)
    objects = models.Manager()
    approved_objects = ApprovedProjectManager()
    unapproved_objects = UnapprovedProjectManager()
    public_objects = PublicProjectManager()

    gitter_room = models.CharField(
        help_text=_('Gitter room name, e.g. gitterhq/sandbox'),
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_gitter_room_name]
    )

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        app_label = 'base'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """Overloaded save method.

        :param args:
        :param kwargs:
        """
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = unicode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        """Return URL to project detail page

        :return: URL
        :rtype: str

        """
        return reverse('project-detail', kwargs={'slug': self.slug})

    def versions(self):
        """Get all the versions for this project."""
        qs = Version.objects.filter(project=self).order_by('-padded_version')
        return qs

    def latest_versions(self):
        """Get the latest version.

        How many versions returned is determined by the pagination threshold.

        :returns: List of versions.
        :rtype: list"""
        return self.versions()[:settings.PROJECT_VERSION_LIST_SIZE]

    def versions_public(self):
        """Get all the approved versions for this project."""
        qs = Version.objects.filter(project=self).filter(approved=True).order_by('-padded_version')
        return qs

    def latest_versions_public(self):
        """Get the latest approved version.

        How many versions returned is determined by the pagination threshold.

        :returns: List of approved versions.
        :rtype: list"""
        return self.versions_public()[:settings.PROJECT_VERSION_LIST_SIZE]

    def administrators(self):
        """Get all administrator for this project."""
        qs = ProjectAdministrator.objects.filter(project=self).order_by('user__username')
        return qs

    def collaborators(self):
        """Get all collaborators for this project."""
        qs = ProjectCollaborator.objects.filter(project=self).order_by('user__username')
        return qs

    def is_administrator(self, user):
        """checking user is administrator"""
        if user.is_staff or user == self.owner:
            return True
        try:
            ProjectAdministrator.objects.get(project=self, user=user)
            return True
        except ProjectAdministrator.DoesNotExist:
            return False

    def is_collaborator(self, user):
        """checking user is collaborator"""
        if user.is_staff or user == self.owner:
            return True
        try:
            ProjectCollaborator.objects.get(project=self, user=user)
            return True
        except ProjectCollaborator.DoesNotExist:
            return False

    @staticmethod
    def pagination_threshold(self):
        """Find out how many versions to list per page.

        :returns: The count of items to show per page as defined in
            settings.PROJECT_VERSION_LIST_SIZE.
        :rtype: int
        """
        return settings.PROJECT_VERSION_LIST_SIZE

    def pagination_threshold_exceeded(self):
        """Check if project version count exceeds pagination threshold.

        :returns: Flag indicating if there are more versions than
            self.threshold.
        :rtype: bool
        """
        if self.versions().count() >= settings.PROJECT_VERSION_LIST_SIZE:
            return True
        else:
            return False
