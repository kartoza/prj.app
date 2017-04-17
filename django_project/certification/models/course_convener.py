# coding=utf-8
"""Course convener model definitions for certification apps.

"""

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from certifying_organisation import CertifyingOrganisation


class CourseConvener(models.Model):
    """Course Convener model."""

    slug = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    user = models.ForeignKey(User)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    objects = models.Manager()

    class Meta:
        ordering = ['user']

    def save(self, *args, **kwargs):
        self.slug = self.user.username
        super(CourseConvener, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        """Return URL to course convener detail page.

        :return: URL
        :rtype: str
        """
        return reverse('course-convener-detail', kwargs={
            'slug': self.slug,
        })
