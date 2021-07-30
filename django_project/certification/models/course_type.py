# coding=utf-8
"""Course type model definitions for certification apps.

"""

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from django.utils.text import slugify
from .certifying_organisation import CertifyingOrganisation


def increment_name(name, registered):
    """Function to increment object name.

    If there are duplicate names, this function will increment it.
    """

    new_name = name
    registered_name = registered.values_list('name', flat=True)
    if name in registered_name:
        counter = registered.filter(name=new_name).count()
        counter += 1
        new_name = '%s %s' % (new_name, counter)

    return new_name


class CourseType(models.Model):
    """Course Type model."""

    name = models.CharField(
        help_text=_('Course type.'),
        max_length=200,
        null=False,
        blank=False
    )

    description = models.TextField(
        help_text=_('Course type description - 1000 characters limit.'),
        max_length=1000,
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

    slug = models.SlugField()
    certifying_organisation = models.ForeignKey(CertifyingOrganisation,
                                                on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'certifying_organisation']

    def save(self, *args, **kwargs):
        if not self.pk:
            registered_course_type = CourseType.objects.all()
            name = increment_name(self.name, registered_course_type)
            words = name.split()
            filtered_words = [word for word in
                              words if word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(CourseType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to course type detail page.

        :return: URL
        :rtype: str
        """
        return reverse('course-type-detail', kwargs={
            'slug': self.slug,
        })
