# coding=utf-8
"""Model for status of the certifying organisation."""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models.project import Project


class Status(models.Model):
    """Status model."""

    name = models.CharField(
        help_text=_('Name of the status'),
        max_length=200,
        null=False,
        blank=False,
    )

    order = models.IntegerField(
        blank=True,
        null=True,
        unique=True
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ['name', 'project']

    def save(self, *args, **kwargs):
        if not self.pk:
            count = Status.objects.all().count()
            self.order = count
        super(Status, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)
