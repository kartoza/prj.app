# coding=utf-8
"""
Course attendee model definitions for certification apps
"""

import string
import random
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from course import Course
from training_center import TrainingCenter
from attendee import Attendee
from django.contrib.auth.models import User


class CourseAttendee(models.Model):

    name = models.CharField(
        help_text="Course attendee.",
        max_length=200,
        null=False,
        blank=False
    )

    slug = models.SlugField()
    attendee = models.ManyToManyField(Attendee)
    training_center = models.ForeignKey(TrainingCenter)
    course = models.ForeignKey(Course)
    # project = models.ForeignKey('base.Project')
    author = models.ForeignKey(User)
    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            name = self.slug_generator()
            words = name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(CourseAttendee, self).save(*args, **kwargs)

    @staticmethod
    def slug_generator(size=6, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to course detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-attendee-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })
