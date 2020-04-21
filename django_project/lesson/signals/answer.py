# coding=utf-8
"""Signal for answer model."""

from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

from lesson.models.answer import Answer
from lesson.signals.utils import update_translation_time_stamp


@receiver(pre_save, sender=Answer)
def worksheet_pre_save(sender, instance, **kwargs):
    update_translation_time_stamp(instance, sender)
