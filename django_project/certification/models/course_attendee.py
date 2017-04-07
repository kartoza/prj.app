# coding=utf-8
"""
Course attendee model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from course import Course
from attendee import Attendee
from django.contrib.auth.models import User


class CourseAttendee(models.Model):

    attendee = models.ManyToManyField(Attendee)
    course = models.ForeignKey(Course)
    author = models.ForeignKey(User)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        super(CourseAttendee, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s: %s' % (self.course.name, str(self.id))

    def get_absolute_url(self):
        """Return URL to course detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-attendee-detail', kwargs={
            'slug': str(self.id),
        })
