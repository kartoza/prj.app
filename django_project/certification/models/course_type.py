# coding=utf-8
"""Course type model definitions for certification apps.

"""

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from certifying_organisation import CertifyingOrganisation, SlugifyingMixin


class CourseType(SlugifyingMixin, models.Model):
    """Course Type model."""

    name = models.CharField(
        help_text=_('Course type.'),
        max_length=200,
        null=False,
        blank=False
    )

    description = models.TextField(
        help_text=_('Course type description.'),
        max_length=250,
        null=True,
        blank=True,
    )

    instruction_hours = models.CharField(
        help_text=_('Number of instruction hours e.g. 40 hours'),
        max_length=200,
        null=True,
        blank=True
    )

    coursetype_link = models.CharField(
        verbose_name='Link',
        help_text='Link to course types e.g. http://kartoza.com/',
        max_length=200,
        null=True,
        blank=True
    )

    slug = models.SlugField(unique=True)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    author = models.ForeignKey(User)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(CourseType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to course type detail page.

        :return: URL
        :rtype: str
        """
        return reverse('course-type-detail', kwargs={
            'slug': self.slug,
        })
