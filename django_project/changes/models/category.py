import logging

from django.core.urlresolvers import reverse
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS

from django.db import models
from django.utils.translation import ugettext_lazy as _
from changes.models.entry import Entry

logger = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
class Category(models.Model):
    """A category model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text=_('Name of this category.'),
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    sort_number = models.SmallIntegerField(
        help_text=(
            'The order in which this category is listed within a '
            'project'),
        default=0
    )
    slug = models.SlugField()
    project = models.ForeignKey('base.Project')
    objects = models.Manager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the category class."""
        unique_together = (
            ('name', 'project'),
            ('project', 'slug')
        )
        app_label = 'changes'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            new_list = ' '.join(filtered_words)
            self.slug = slugify(new_list)[:50]
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })

    def has_entries(self):
        """Does this Category have related Entries?

        :return: True or False
        :rtype: bool
        """
        if Entry.objects.filter(category=self).exists():
            return True
        else:
            return False
