# coding=utf-8
"""Certificate model definitions for certification apps.

"""

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from course import Course
from attendee import Attendee


def increment_id(project):
    """Increment the certificate ID."""

    last_certificate = Certificate.objects.filter(
        course__certifying_organisation__project=project
    ).count()
    if last_certificate == 0:
        return '1'
    last_int_id = last_certificate
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

    is_paid = models.BooleanField(
        help_text=_('Is this certificate paid?'),
        default=False
    )

    author = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    attendee = models.ForeignKey(Attendee)
    objects = models.Manager()

    class Meta:
        ordering = ['certificateID']
        unique_together = [
            'course', 'attendee', 'certificateID',
        ]

    def __unicode__(self):
        return self.certificateID

    def save(self, *args, **kwargs):
        if self.int_id is None:
            project_name = self.course.certifying_organisation.project.name
            words = project_name.replace(' ', '')
            increment_certificate = \
                increment_id(self.course.certifying_organisation.project)
            self.certificateID = '%s-%s' % (words, str(increment_certificate))
        super(Certificate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to certificate detail page.

        :return: URL
        :rtype: str
        """
        return reverse('certificate-detail', kwargs={
            'slug': self.certificateID,
        })
