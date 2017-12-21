# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
import os


ROLE = (
    ('project', 'project'),
    ('organisation', 'organisation'),
)


class Domain(models.Model):
    """Model to save subscribed user and their custom domain."""

    user = models.ForeignKey(User)
    role = models.CharField(
        choices=ROLE,
        default='project',
        blank=False,
        null=False,
        max_length=30
    )
    domain = models.CharField(
        help_text=_('Custom domain, i.e. www.kartoza.com'),
        max_length=30,
        null=False,
        blank=False,
        unique=True,
    )
    approved = models.BooleanField(
        help_text=_('Whether this user domain has been approved for use yet.'),
        default=False
    )

    class Meta:
        ordering = ['domain']

    def save(self, *args, **kwargs):
        super(Domain, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.domain
