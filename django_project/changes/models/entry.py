# coding=utf-8
"""Models for changelog entries."""
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
import os
import logging
from core.settings.contrib import STOP_WORDS
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class Entry(models.Model):
    """An entry is the basic unit of a changelog."""

    sequence_number = models.IntegerField(
        verbose_name=_('Entry number'),
        help_text=_(
            'The order in which this entry is listed within the category.'),
        blank=False,
        null=False,
        default=0
    )

    title = models.CharField(
        help_text='Feature title for this changelog entry.',
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # Unique together rule applies in meta class

    description = models.TextField(
        null=True,
        blank=True,
        help_text='Describe the new feature. Markdown is supported.')

    image_file = models.ImageField(
        help_text=(
            'A image that is related to this visual changelog entry. '
            'Most browsers support dragging the image directly on to the '
            '"Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/entries'),
        blank=True)

    image_credits = models.CharField(
        help_text='Who should be credited for this image?',
        max_length=255,
        null=True,
        blank=True)

    video = EmbedVideoField(
        verbose_name='Youtube video',
        help_text='Paste your youtube video link',
        null=True,
        blank=True)

    funded_by = models.CharField(
        help_text='Input the funder name.',
        max_length=255,
        null=True,
        blank=True)

    funder_url = models.CharField(
        help_text='Input the funder URL.',
        max_length=255,
        null=True,
        blank=True)

    developed_by = models.CharField(
        help_text='Input the developer name.',
        max_length=255,
        null=True,
        blank=True)

    developer_url = models.CharField(
        help_text='Input the developer URL.',
        max_length=255,
        null=True,
        blank=True)

    github_PR_url = models.CharField(
        help_text='Input the Github PR URL when applicable.',
        max_length=255,
        null=True,
        blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    # noinspection PyUnresolvedReferences
    version = models.ForeignKey('Version', on_delete=models.CASCADE)
    # noinspection PyUnresolvedReferences
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    objects = models.Manager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the version class."""
        unique_together = (
            ('title', 'version', 'category'),
            ('version', 'slug'),
        )
        ordering = ['version', 'category', 'sequence_number']
        app_label = 'changes'

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.title.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]

            # Sequence number
            max_number = Entry.objects.all().\
                filter(version=self.version, category=self.category).aggregate(
                models.Max('sequence_number'))
            max_number = max_number['sequence_number__max']
            # We take the maximum number. If the table is empty, we let the
            # default value defined in the field definitions.
            if max_number is not None:
                self.sequence_number = max_number + 1

        super(Entry, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('entry-detail', kwargs={
            'pk': self.id
        })

    def funder_info_html(self):
        string = ""
        if self.funded_by and self.funder_url is None:
            string = ""
            return string
        elif self.funded_by and not self.funder_url:
            string = "This feature was funded by %s " % self.funded_by
            return string
        elif self.funder_url and not self.funded_by:
            string = "This feature was funded by [%s](%s)" % (
                self.funder_url, self.funder_url)
            return string
        elif self.funded_by and self.funder_url:
            string = "This feature was funded by [%s](%s)" % (
                self.funded_by, self.funder_url)
            return string
        else:
            return string

    def developer_info_html(self):
        string = ""
        if self.developed_by and self.developer_url is None:
            string = ""
            return string
        elif self.developed_by and not self.developer_url:
            string = "This feature was developed by %s " % self.developed_by
            return string
        elif self.developer_url and not self.developed_by:
            string = "This feature was developed by [%s](%s)" % (
                self.developer_url, self.developer_url)
            return string
        elif self.developed_by and self.developer_url:
            string = "This feature was developed by [%s](%s)" % (
                self.developed_by, self.developer_url)
            return string
        else:
            return string
