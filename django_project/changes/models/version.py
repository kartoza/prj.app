# coding=utf-8
import re
from django.urls import reverse
from common.utilities import version_slugify
import os
import logging
from .entry import Entry
from .sponsorship_period import SponsorshipPeriod
from core.settings.contrib import STOP_WORDS
from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models
from ..utils.custom_slugfield import CustomSlugField

logger = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
class Version(models.Model):
    """A version model that the changelog is associated with.."""

    name = models.CharField(
        help_text='Name of this release e.g. 1.0.1.',
        max_length=255,
        null=False,
        blank=False,
        unique=False)

    padded_version = models.CharField(
        help_text=(
            'Numeric version for this release e.g. 001000001 for 1.0.1 '
            'calculated by zero padding each component of maj/minor/bugfix '
            'elements from name.'),
        max_length=9,
        null=False,
        blank=True,
        unique=False)

    image_file = models.ImageField(
        help_text=(
            'An optional image for this version e.g. a splashscreen. '
            'Most browsers support dragging the image directly on to the '
            '"Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=True)

    description = models.TextField(
        null=True,
        blank=True,
        help_text='Describe the new version. Markdown is supported.')

    release_date = models.DateField(
        _('Release date (yyyy-mm-dd)'),
        help_text='Date of official release',
        null=True,
        blank=True)

    locked = models.BooleanField(
        default=False,
        help_text='Whether this version is locked for editing.',
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = CustomSlugField()
    project = models.ForeignKey('base.Project', on_delete=models.CASCADE)
    objects = models.Manager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the version class."""
        unique_together = (
            ('name', 'project'),
            ('slug', 'project'),
        )
        app_label = 'changes'
        # ordering = ['-datetime_created']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = version_slugify(new_list)[:50]
        self.padded_version = self.pad_name(str(self.get_numerical_name()))
        super(Version, self).save(*args, **kwargs)

    def get_numerical_name(self):
        name = self.name
        non_decimal = re.compile(r'[^\d.]+')
        numeric_name = non_decimal.sub('', name)
        number = numeric_name.split('.')

        # Fix the numbering of the version name to have format: 0.0.0.
        while len(number) < 3:
            numeric_name += '.0'
            number = numeric_name.split('.')
        return numeric_name

    def pad_name(self, version):
        """Create a 0 padded version of the version name.

        e.g. input: 2.10.1
        e.g. output: 002010100

        This will ensure we have sortable version names.

        :param version: A text version in the form 0.0.0 - if the version is
            not in this form, we return the version unaltered.
        :type version: str

        :returns: Zero padded representation of the version e.g. 001010100
        :rtype: str

        """
        tokens = version.split('.')
        if len(tokens) != 3:
            return version
        result = ''
        for token in tokens:
            result += token.zfill(3)
        return result

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)

    def get_absolute_url(self):
        return reverse('version-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })

    def entries(self):
        """Get the entries for this version."""
        qs = Entry.objects.filter(
            version=self).order_by('category__sort_number')
        return qs

    def _entries_for_category(self, category):
        """All entries for this version and filtered by the given category.

        :param category: Category to filter by.
        :type category: Category
        """
        qs = Entry.objects.filter(version=self, category=category)
        return qs

    def categories(self):
        """Get a list of categories where there are one or more entries.

        Example use in template::
            {% for row in version.categories %}
              <h2 class="text-muted">{{ row.category.name }}</h2>
              <ul>
              {%  for entry in row.entries %}
                 <li>{{ entry.name }}</li>
              {% endfor %}
              </ul>
            {% endfor %}
        """
        qs = self.entries()
        used = []
        categories = []
        for entry in qs:
            category = entry.category
            if category not in used:
                row = {
                    'category': category,
                    'entries': self._entries_for_category(category)
                }
                categories.append(row)
                used.append(category)
        return categories

    def sponsors(self):
        """Return a list of sponsors current at time of this version release.

        :returns: A list of SponsorPeriod objects for current project
            whose release date coincides with the version release date.
            Only approved sponsors are returned.
            Returns None if the release date (which is optional) is not set.
        :rtype: Queryset, None
        """
        if self.release_date is None:
            return None
        sponsors = SponsorshipPeriod.approved_objects.filter(
                end_date__gte=self.release_date).filter(
                start_date__lte=self.release_date).filter(
                project=self.project).order_by(
            'start_date').order_by(
            '-sponsorship_level__value', 'sponsor__name')
        return sponsors

    def formatted_release_date(self):
        """"Return a long formatted released date e.g. 24 June 2016.

        :returns: A string containing the long formatted date, or an empty
            string if the date is not set.
        :rtype: str
        """
        long_date = None
        if self.release_date:
            # %-d Day of the month as a decimal number. (Platform specific)
            # %B  Month as locale’s full name.
            # %Y  Year e.g. 2016
            long_date = self.release_date.strftime('%-d %B, %Y')
        return long_date
