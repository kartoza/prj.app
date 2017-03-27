# coding=utf-8
"""
Certificate model definitions for certification apps
"""

import random
import string
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from django.contrib.auth.models import User
from course_attendee import CourseAttendee
from course import Course


class Certificate(models.Model):
    """Certificate model."""

    certificateID = models.CharField(
        help_text="Id certificate.",
        max_length=200,
        blank=False,
        null=False,
    )

    slug = models.SlugField()
    author = models.ForeignKey(User)
    # project = models.ForeignKey('base.Project')
    course_attendee = models.ForeignKey(CourseAttendee)
    course = models.ForeignKey(Course)
    objects = models.Manager()

    class Meta:
        ordering = ['certificateID']

    def save(self, *args, **kwargs):
        if not self.pk:
            certificateID = self.slug_generator()
            words = certificateID.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]

        super(Certificate, self).save(*args, **kwargs)

    @staticmethod
    def slug_generator(size=6, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def __unicode__(self):
        return self.certificateID

    def get_absolute_url(self):
        """Return URL to certificate detail page.
        :return: URL
        :rtype: str
        """
        return reverse('certificate-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })
