# coding=utf-8
"""
Certificate model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from course import Course
from attendee import Attendee


def increment_id():
    last_certificate = Certificate.objects.all().order_by('int_id').last()
    if not last_certificate:
        return '1'
    last_int_id = last_certificate.int_id
    new_int_id = last_int_id + 1
    return new_int_id


class Certificate(models.Model):
    """Certificate model."""

    int_id = models.AutoField(primary_key=True)
    certificateID = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    author = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    attendee = models.ForeignKey(Attendee)
    objects = models.Manager()

    class Meta:
        ordering = ['certificateID']

    def __unicode__(self):
        return self.certificateID

    def save(self, *args, **kwargs):
        project_name = self.course.certifying_organisation.project.name
        int_id = increment_id()
        self.certificateID = project_name + '-' + str(int_id)
        super(Certificate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to certificate detail page.
        :return: URL
        :rtype: str
        """
        return reverse('certificate-detail', kwargs={
            'slug': self.certificateID,
        })
