# coding=utf-8
"""
Course convener model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from django.db import models

from unidecode import unidecode
from django.contrib.auth.models import User
from certifying_organisation import CertifyingOrganisation


class CourseConvener(models.Model):
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
    objects = models.Manager()
    author = models.ForeignKey(User)
    # project = models.ForeignKey('base.Project')
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

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
