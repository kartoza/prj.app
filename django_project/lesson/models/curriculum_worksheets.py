# coding=utf-8

"""Curriculum model definitions for lesson apps."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lesson.models.curriculum import Curriculum
from lesson.models.worksheet import Worksheet


class CurriculumWorksheets(models.Model):
    """Many to many relationship."""
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
    )

    worksheet = models.ForeignKey(
        Worksheet,
        on_delete=models.CASCADE,
    )

    sequence_number = models.IntegerField(
        verbose_name=_('Worksheet number'),
        help_text=_(
            'The order in which this worksheet is listed within a curriculum'),
        blank=False,
        null=False,
        default=0,
    )

    def __str__(self):
        return "{0} : {1}".format(self.curriculum, self.worksheet)
