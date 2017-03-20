# coding=utf-8
"""
Attendee model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from certificate import Certificate
from django.utils.text import slugify


class Attendee(models.Model):
    """Course Attendee model."""

    firstname = models.CharField(
        help_text="First name course attendee.",
        max_length=200,
        null=False,
        blank=False
    )

    surname = models.CharField(
        help_text="Surname course attendee.",
        max_length=200,
        null=False,
        blank=False
    )

    email = models.CharField(
        help_text="Email address.",
        max_length=200,
        null=False,
        blank=False
    )

    slug = models.SlugField()
    objects = models.Manager()
    certificate = models.ForeignKey(Certificate)

    # noinspection PyClassicStyleClass.
    class Meta:
        """ Meta class for Course attendee."""

        ordering = ['firstname']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.firstname.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(Attendee, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.firstname

    def get_absolute_url(self):
        """Return URL to attendee detail page.
        :return: URL
        :rtype: str
        """
        return reverse('attendee-detail', kwargs={'slug': self.slug})
