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

    partners = models.BooleanField(
        default=False,
        help_text=_('Funders or Partners of this project.')
    )

    integrations = models.BooleanField(
        default=False,
        help_text=_('Project integrations, e.g. Travis CI.')
    )

    sponsor = models.BooleanField(
        default=False,
        help_text=_('Sponsor of the project.')
    )

    donations = models.BooleanField(
        default=False,
        help_text=_('Donations for this project.')
    )

    bug_bounties = models.BooleanField(
        default=False,
        help_text=_('Bug bounties for this project.')
    )

    crowd_funding = models.BooleanField(
        default=False,
        help_text=_('Crowd funding for this project.')
    )

    certification = models.BooleanField(
        default=False,
        help_text=_('Certification app of this project.')
    )

    service_providers = models.BooleanField(
        default=False,
        help_text=_('Service providers of this project.')
    )

    store = models.BooleanField(
        default=False,
        help_text=_('Store that sells items/merchandise of this project.')
    )

    changelog = models.BooleanField(
        default=True,
        help_text=_('Changelog app of this project (releases).')
    )

    developer_map = models.BooleanField(
        default=True,
        help_text=_('Developers who build this project.')
    )

    user_map = models.BooleanField(
        default=True,
        help_text= _('Users')
    )

    upcoming_events = models.BooleanField(
        default=True,
        help_text=_('News and upcoming events.')
    )

    project_teams = models.BooleanField(
        default=True,
        help_text=_('Project Teams')
    )

    votes = models.BooleanField(
        default=True,
        help_text=_('Votes')
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
