# coding=utf-8
"""
Certificate model definitions for certification apps
"""

import random
import string
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS


class Certificate(models.Model):
    """Certificate model."""

    id_id = models.CharField(
        help_text="Id certificate.",
        max_length=200,
        blank=False,
        null=False,
    )

    slug = models.SlugField()
    objects = models.Manager()

    class Meta:
        """ Meta class for Certificate."""

        ordering = ['id_id']

    def __unicode__(self):
        return u'%s' % self.id_id

    def save(self, *args, **kwargs):

        if not self.pk:
            id_id = self.slug_generator()
            words = id_id.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(Certificate, self).save(*args, **kwargs)

    @staticmethod
    def slug_generator(size=6, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_absolute_url(self):
        """Return URL to certificate detail page.
        :return: URL
        :rtype: str
        """
        return reverse('certificate-detail', kwargs={'slug': self.slug})
