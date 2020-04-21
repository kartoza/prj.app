# coding=utf-8
"""Signal for worksheet question model."""

from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

from lesson.models.worksheet_question import WorksheetQuestion
from lesson.signals.utils import update_translation_time_stamp


@receiver(pre_save, sender=WorksheetQuestion)
def worksheet_pre_save(sender, instance, **kwargs):
    update_translation_time_stamp(instance, sender)
