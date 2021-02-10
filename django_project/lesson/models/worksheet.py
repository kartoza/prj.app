# coding=utf-8
"""Worksheet model definitions for lesson apps.

"""
import os
import logging

from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import FieldTracker

from lesson.models.mixins import TranslationMixin
from lesson.models.license import License
from lesson.models.section import Section
from lesson.utilities import custom_slug

logger = logging.getLogger(__name__)


class PublishedWorksheetManager(models.Manager):
    """Custom worksheet manager that shows only published worksheet."""

    def get_queryset(self):
        """Query set generator."""
        return super(PublishedWorksheetManager, self).get_queryset().filter(
            published=True)


class Worksheet(TranslationMixin):
    """Worksheet lesson model."""

    tracker = FieldTracker()

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    license = models.ForeignKey(License,
                                blank=True,
                                null=True,
                                on_delete=models.CASCADE)

    sequence_number = models.IntegerField(
        verbose_name=_('Worksheet number'),
        help_text=_(
            'The order in which this worksheet is listed within a section'),
        blank=False,
        null=False,
        default=0
    )

    module = models.CharField(
        help_text=_('Name of worksheet.'),
        blank=False,
        null=False,
        max_length=200,
    )

    title = models.CharField(
        help_text=_('Title of module.'),
        blank=False,
        null=False,
        max_length=200,
    )

    summary_leader = models.CharField(
        help_text=_('Title of the summary.'),
        blank=False,
        null=False,
        max_length=200,
    )

    summary_text = models.TextField(
        help_text=_('Content of the Summary. Markdown is supported. '
                    'Add the following text to insert a page break in the '
                    'PDF output: a &ltdiv class="page-break"&gt&lt/div&gt '
                    'element between sections of the content.'),
        blank=False,
        null=False,
    )

    summary_image = models.ImageField(
        help_text=_('Image of the summary. A landscape image, approximately '
                    '800*200. Most browsers support dragging the image '
                    'directly on to the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet/summary_image'),
        blank=True
    )

    exercise_goal = models.CharField(
        help_text=_('The goal of the exercise.'),
        blank=True,
        null=True,
        max_length=200,
    )

    exercise_task = models.TextField(
        help_text=_('Task in the exercise. Markdown is supported.'),
        blank=True,
        null=True,
    )

    exercise_image = models.ImageField(
        help_text=_('Image for the exercise part. You should normally either '
                    'use the Requirements table or this image field. '
                    'A landscape image, approximately 800*200. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet/exercise'),
        blank=True
    )

    more_about_title = models.CharField(
        help_text=_('More about title.'),
        blank=True,
        null=True,
        max_length=200,
        default=_('More about'),
    )

    more_about_text = models.TextField(
        help_text=_(
            'More detail about the content of the worksheet. '
            'Markdown is supported.'),
        blank=True,
        null=True,
    )

    more_about_image = models.ImageField(
        help_text=_('Image for the more about part. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet/more_about'),
        blank=True
    )

    external_data = models.FileField(
        help_text=_('External data used in this worksheet. Usually a ZIP '
                    'file. Most browsers support dragging the file directly '
                    'on to the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/lesson/worksheet/external_data'),
        blank=True
    )
    youtube_link = models.URLField(
        help_text=_('Link to a YouTube video.'),
        null=True,
        blank=True
    )
    author_name = models.CharField(
        help_text=_('The author of this worksheet.'),
        blank=True,
        null=True,
        max_length=200,
    )
    author_link = models.URLField(
        help_text=_('Link to the author webpage.'),
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    requirement_header_name_first = models.CharField(
        help_text=_('Set header name of the first column in requirements '
                    'table questions. Markdown is supported.'),
        blank=True,
        null=True,
        max_length=200,
    )

    requirement_header_name_last = models.CharField(
        help_text=_('Set header name of the last column in requirements '
                    'table questions. Markdown is supported.'),
        blank=True,
        null=True,
        max_length=200,
    )


    summary_image_dimension = models.CharField(
        help_text=_('Set the height and width of summary_image element '
                    'in a css format. e.g <b>height: 200px; width: 300px;</b>.'
                    ' The value will be added onto image style attribute in '
                    'the PDF output.'),
        blank=True,
        null=True,
        max_length=200
    )

    exercise_image_dimension = models.CharField(
        help_text=_('Set the height and width of exercise_image element '
                    'in a css format. e.g <b>height: 200px; width: 300px;</b>.'
                    ' The value will be added onto image style attribute in '
                    'the PDF output.'),
        blank=True,
        null=True,
        max_length=200
    )

    more_about_image_dimension = models.CharField(
        help_text=_('Set the height and width of more_about_image element '
                    'in a css format. e.g <b>height: 200px; width: 300px;</b>.'
                    ' The value will be added onto image style attribute in '
                    'the PDF output.'),
        blank=True,
        null=True,
        max_length=200
    )

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

    published = models.BooleanField(
        help_text=_(
            'Whether this worksheet is visible for public.'),
        default=False,
        null=False,
        blank=False
    )

    page_break_before_exercise = models.BooleanField(
        help_text=_(
            'Check if you wish a page break before the Exercise content.'),
        default=False,
        null=False,
        blank=False
    )
    page_break_before_requirement_table = models.BooleanField(
        help_text=_(
            'Check if you wish a page break before the Requirement table.'),
        default=False,
        null=False,
        blank=False
    )
    page_break_before_exercise_image = models.BooleanField(
        help_text=_(
            'Check if you wish a page break before the Exercise image.'),
        default=False,
        null=False,
        blank=False
    )
    page_break_before_more_about = models.BooleanField(
        help_text=_(
            'Check if you wish a page break before the More About content.'),
        default=False,
        null=False,
        blank=False
    )
    page_break_before_question = models.BooleanField(
        help_text=_(
            'Check if you wish a page break before the Question content.'),
        default=False,
        null=False,
        blank=False
    )
    page_break_before_youtube_link = models.BooleanField(
        help_text=_(
            'Check if you wish a page break before the YouTube Link.'),
        default=False,
        null=False,
        blank=False
    )
    page_break_before_further_reading = models.BooleanField(
        help_text=_(
            'Check if you wish a page break before the Further Reading '
            'content.'),
        default=False,
        null=False,
        blank=False
    )

    objects = models.Manager()
    published_objects = PublishedWorksheetManager()

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for Worksheet model."""

        app_label = 'lesson'
        ordering = ['section', 'sequence_number']
        # Need to fix the transaction integrity after we submit a new order.
        # https://stackoverflow.com/questions/40891574/how-can-i-set-a-
        # table-constraint-deferrable-initially-deferred-in-django-model
        # unique_together = ['section', 'sequence_number']

    def funder_info_html(self):
        string = ""
        if self.funded_by and self.funder_url is None:
            string = ""
            return string
        elif self.funded_by and not self.funder_url:
            string = "This lesson was funded by %s " % self.funded_by
            return string
        elif self.funder_url and not self.funded_by:
            string = "This lesson was funded by [%s](%s)" % (
                self.funder_url, self.funder_url)
            return string
        elif self.funded_by and self.funder_url:
            string = "This lesson was funded by [%s](%s)" % (
                self.funded_by, self.funder_url)
            return string
        else:
            return string

    def save(self, *args, **kwargs):
        is_new_record = False if self.pk else True
        if is_new_record:
            # Default slug
            self.slug = custom_slug(self.module)

            # Section number
            max_number = Worksheet.objects.all().\
                filter(section=self.section).aggregate(
                models.Max('sequence_number'))
            max_number = max_number['sequence_number__max']
            # We take the maximum number. If the table is empty, we let the
            # default value defined in the field definitions.
            if max_number is not None:
                self.sequence_number = max_number + 1

        super(Worksheet, self).save(*args, **kwargs)

        if is_new_record:
            # We update the slug field with its ID and we save it again.
            self.slug = '{}-{}'.format(custom_slug(self.module), self.pk)[:50]
            self.save()

    def __unicode__(self):
        return self.module

    def __str__(self):
        return self.module

from lesson.signals.worksheet import *  # noqa
