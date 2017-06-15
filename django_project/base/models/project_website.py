# coding=utf-8
import os
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _
from project import Project
from changes.models.sponsor import Sponsor


class ProjectWebsite(models.Model):
    """Project website model."""

    name = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    image = models.ImageField(
        help_text=_('A screenshot/diagram for this project. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/project_web'),
        blank=True
    )

    precis = models.TextField(
        max_length=3000,
        help_text=_('Abstract/summary of the project.'),
        blank=True
    )

    partners = models.TextField(
        max_length=3000,
        blank=True,
        help_text=_('Funders or Partners of this project.')
    )

    integrations = models.CharField(
        max_length=1000,
        blank=True,
        help_text=_('Project integrations, e.g. Travis CI.')
    )

    slug = models.SlugField(blank=True)
    project = models.ForeignKey(Project)

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Project Website."""

        app_label = 'base'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = self.project.name
            self.slug = '%s-web' % self.project.slug
        super(ProjectWebsite, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def sponsors(self):
        """Get all the sponsors for this project."""
        qs = Sponsor.objects.filter(project=self.project).order_by('name')
        return qs
