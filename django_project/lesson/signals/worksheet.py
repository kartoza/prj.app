# coding=utf-8
"""Signal for worksheet model."""

import datetime

from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

from modeltranslation.translator import translator

from lesson.models.worksheet import Worksheet


@receiver(pre_save, sender=Worksheet)
def worksheet_pre_save(sender, instance, **kwargs):
    # New instance, always set the last_update
    if instance.pk is None:
        instance.last_update = datetime.datetime.now()
        return
    need_update_timestamp = False
    translated_fields = translator.get_options_for_model(
        Worksheet).get_field_names()
    for translated_field in translated_fields:
        if instance.tracker.has_changed(translated_field):
            need_update_timestamp = True
            break
    if need_update_timestamp:
        instance.last_update = datetime.datetime.now()
