# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Organisation(models.Model):
    """Organisation where the project belongs."""

    name = models.CharField(
        help_text=_('Name of this organisation.'),
        max_length=150,
        null=False,
        blank=False,
        unique=True
    )

    approved = models.BooleanField(
        help_text=_('Whether this organisation has been approved for use yet.'),
        default=False
    )

    owner = models.ForeignKey(User, null=True, blank=True)

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(Organisation, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.name)
