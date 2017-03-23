# coding=utf-8
"""
Course type model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from course import Course


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
    course = models.ManyToManyField(Course)

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Course types."""

        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(CourseType, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        """Return URL to course type detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-type-detail', kwargs={'slug': self.slug})
