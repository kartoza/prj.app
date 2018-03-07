# coding=utf-8
"""Signal for further reading model."""

from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

from lesson.models.further_reading import FurtherReading
from lesson.signals.utils import update_translation_time_stamp


@receiver(pre_save, sender=FurtherReading)
def worksheet_pre_save(sender, instance, **kwargs):
    update_translation_time_stamp(instance, sender)
