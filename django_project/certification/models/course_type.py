# coding=utf-8
"""
Course type model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from certifying_organisation import CertifyingOrganisation
from django.contrib.auth.models import User


class CourseType(models.Model):
    """Course Type model."""

    name = models.CharField(
        help_text="Course type.",
        max_length=200,
        null=False,
        blank=False
    )

    slug = models.SlugField(unique=True)
    objects = models.Manager()
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    author = models.ForeignKey(User)
    # project = models.ForeignKey('base.Project')

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Course types."""
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(CourseType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to course type detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-type-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })
