# coding=utf-8
"""Course convener model definitions for certification apps.

"""

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from certifying_organisation import CertifyingOrganisation


class CourseConvener(models.Model):
    """Course Convener model."""

    slug = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    user = models.ForeignKey(User)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    objects = models.Manager()

    class Meta:
        ordering = ['user']

    def save(self, *args, **kwargs):
        words = self.certifying_organisation.name.split()
        filtered_words = [word for word in words if
                          word.lower() not in STOP_WORDS]
        # unidecode() represents special characters (unicode data) in ASCII
        new_list = '%s-%s' % \
                   (self.user.username, unidecode(' '.join(filtered_words)))
        self.slug = slugify(new_list)[:50]
        super(CourseConvener, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        """Return URL to course convener detail page.

        :return: URL
        :rtype: str
        """
        return reverse('course-convener-detail', kwargs={
            'slug': self.slug,
        })
