# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Project, Organisation


ROLE = (
    ('Project', 'Project'),
    ('Organisation', 'Organisation'),
)


class Domain(models.Model):
    """Model to save subscribed user and their custom domain."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(
        help_text=_(
            'For organisation, domain will point to list of projects within '
            'the organisation and for project, domain will only point to '
            'a specific project.'),
        choices=ROLE,
        default='project',
        blank=False,
        null=False,
        max_length=30
    )

    domain = models.CharField(
        help_text=_('Custom domain, i.e. projecta.kartoza.com.'),
        max_length=30,
        null=False,
        blank=False,
        unique=True,
    )

    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    organisation = models.ForeignKey(
        Organisation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    approved = models.BooleanField(
        help_text=_('Whether this domain has been approved for use yet.'),
        default=False
    )

    paid = models.BooleanField(
        help_text=_('Whether this domain has been paid for use yet.'),
        default=False
    )

    class Meta:
        ordering = ['domain']

    def save(self, *args, **kwargs):
        super(Domain, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.domain

    def __str__(self):
        return '{domain} - {project}'.format(
            domain=self.domain,
            project=self.project
        )
