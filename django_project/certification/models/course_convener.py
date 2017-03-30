# coding=utf-8
"""
Course convener model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from certifying_organisation import CertifyingOrganisation, SlugifyingMixin


class CourseConvener(SlugifyingMixin, models.Model):
    """Course Convener model."""

    name = models.CharField(
        help_text="Course convener name",
        max_length=250,
        null=False,
        blank=False,
    )

    email = models.CharField(
        help_text="Course convener email",
        max_length=150,
        null=True,
        blank=True,
    )

    slug = models.SlugField()
    author = models.ForeignKey(User)
    project = models.ForeignKey('base.Project', to_field='name')
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(CourseConvener, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to course convener detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-convener-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })
