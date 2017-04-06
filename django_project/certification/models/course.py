# coding=utf-8
"""
Course model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from course_convener import CourseConvener
from certifying_organisation import CertifyingOrganisation, SlugifyingMixin
from course_type import CourseType
from training_center import TrainingCenter
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger(__name__)


class Course(SlugifyingMixin, models.Model):
    """Course model."""

    name = models.CharField(
        help_text="Course name.",
        max_length=200,
        null=False,
        blank=False,
    )

    start_date = models.DateField(
        _("Start date"),
        help_text='Course start date',
        default=timezone.now)

    end_date = models.DateField(
        _("End date"),
        help_text='Course end date',
        default=timezone.now)

    slug = models.SlugField()
    course_convener = models.ForeignKey(CourseConvener)
    course_type = models.ForeignKey(CourseType)
    training_center = models.ForeignKey(TrainingCenter)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    author = models.ForeignKey(User)
    # project = models.ForeignKey('base.Project')
    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to course detail page.
        :return: URL
        :rtype: str
        """
        return reverse('course-detail', kwargs={
            'slug': self.slug,
            'certifyingorganisation_slug': self.certifying_organisation.slug
        })
