# coding=utf-8
"""
Course convener model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from certifying_organisation import CertifyingOrganisation
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS


class CourseConvener(models.Model):
    """Course Convener model."""

    slug = models.SlugField()
    name = models.ForeignKey(User)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            convener_name = self.name.username
            words = convener_name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]

        super(CourseConvener, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name.username

    def get_absolute_url(self):
        """Return URL to course convener detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-convener-detail', kwargs={
            'slug': self.slug,
        })
