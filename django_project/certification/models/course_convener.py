# coding=utf-8
"""
Course convener model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from course import Course


class CourseConvener(models.Model):
    """Course Convener model."""

    slug = models.SlugField()
    objects = models.Manager()
    course = models.ManyToManyField(Course)

    def get_absolute_url(self):
        """Return URL to course convener detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-convener-detail', kwargs={'slug': self.slug})
