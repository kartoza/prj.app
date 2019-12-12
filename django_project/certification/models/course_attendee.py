# coding=utf-8
"""Course attendee model definitions for certification apps.

"""

from django.db import models
from django.contrib.auth.models import User
from certification.models.course import Course
from certification.models.attendee import Attendee


class CourseAttendee(models.Model):
    """One person who attends course is defined here."""

    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        unique_together = (('attendee', 'course'),)

    def save(self, *args, **kwargs):
        super(CourseAttendee, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s: %s' % (self.course.name, str(self.id))
