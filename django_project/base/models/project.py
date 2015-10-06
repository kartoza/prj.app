# coding=utf-8
"""Project model used by all apps."""
import os
import logging
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _
from audited_models.models import AuditedModel
from changes.models.version import Version
from core.settings.contrib import STOP_WORDS
from django.contrib.auth.models import User

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

    owner = models.ForeignKey(User)
    slug = models.SlugField(unique=True)
    objects = models.Manager()
    approved_objects = ApprovedProjectManager()
    unapproved_objects = UnapprovedProjectManager()
    public_objects = PublicProjectManager()
    threshold = '2'

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

    def more_than_threshold(self):
        """Check Count Number of versions for this project
        whether more than threshold or not."""
        if self.versions().count() >= int(self.threshold):
            return True
