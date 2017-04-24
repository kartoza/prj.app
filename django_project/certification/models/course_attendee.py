# coding=utf-8
"""Course attendee model definitions for certification apps.

"""

from django.db import models
from course import Course
from attendee import Attendee
from django.contrib.auth.models import User


class CourseAttendee(models.Model):
    """One person who attends course is defined here."""

    attendee = models.ForeignKey(Attendee)
    course = models.ForeignKey(Course)
    author = models.ForeignKey(User)
    objects = models.Manager()

    class Meta:
        unique_together = (('attendee', 'course'),)

    def save(self, *args, **kwargs):
        super(CourseAttendee, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s: %s' % (self.course.name, str(self.id))
