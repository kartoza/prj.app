from django.core.urlresolvers import reverse
from django.utils.text import slugify
import os
import logging
from core.settings.contrib import STOP_WORDS

logger = logging.getLogger(__name__)
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from audited_models.models import AuditedModel
from .entry import Entry
from django.contrib.auth.models import User


class ApprovedVersionManager(models.Manager):
    """Custom version manager that shows only approved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedVersionManager, self).get_query_set().filter(
                approved=True)


class UnapprovedVersionManager(models.Manager):
    """Custom version manager that shows only unapproved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            UnapprovedVersionManager, self).get_query_set().filter(
                approved=False)


class Version(AuditedModel):
    """A version model that the changelog is associated with.."""
    name = models.CharField(
        help_text='Name of this release e.g. 1.0.1.',
        max_length=255,
        null=False,
        blank=False,
        unique=False)

    approved = models.BooleanField(
        help_text=(
            'Whether this version has been approved for use by the '
            'project owner.'),
        default=False)

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

    author = models.ForeignKey(User)
    slug = models.SlugField()
    project = models.ForeignKey('base.Project')
    objects = models.Manager()
    approved_objects = ApprovedVersionManager()
    unapproved_objects = UnapprovedVersionManager()

    class Meta:
        """Meta options for the version class."""
        unique_together = (
            ('name', 'project'),
            ('slug', 'project'),
        )
        app_label = 'changes'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(Version, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)

    def get_absolute_url(self):
        return reverse('version-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })

    def entries(self):
        """Get the entries for this version."""
        qs = Entry.objects.filter(version=self).order_by('category')
        return qs

    def _entries_for_category(self, category):
        """All entries for this version and filtered by the given category.

        :param category: Category to filter by.
        :type category: Category

        .. note:: only approved entries returned.
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
                    'entries': self._entries_for_category(category)}
                categories.append(row)
                used.append(category)
        return categories
