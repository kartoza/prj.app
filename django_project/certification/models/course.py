# coding=utf-8
"""
Course model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from attendee import Attendee, Certificate


class Course(models.Model):
    """Course model."""

    name = models.CharField(
        help_text="Course name.",
        max_length=200,
        null=False,
        blank=False,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(Course, self).save(*args, **kwargs)

    slug = models.SlugField()
    objects = models.Manager()
    course_attendee = models.ManyToManyField(Attendee)
    certificate = models.ManyToManyField(Certificate)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        """Return URL to course detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-detail', kwargs={'slug': self.slug})
