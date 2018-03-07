# coding=utf-8
"""Signal utils."""
import datetime

from modeltranslation.translator import translator


def update_translation_time_stamp(instance, class_model):
    """Update last update time stamp.

    This method is used inside a signal.

    Class model should have field tracker.

    :param instance: The instance of the class.
    :type instance: TranslationMixin

    :param class_model: The sender of the signal / the class of instance.
    :type class_model: class
    """
    # New instance, always set the last_update
    if instance.pk is None:
        instance.last_update = datetime.datetime.now()
        return
    need_update_timestamp = False
    translated_fields = translator.get_options_for_model(
        class_model).get_field_names()
    for translated_field in translated_fields:
        if instance.tracker.has_changed(translated_field):
            need_update_timestamp = True
            break
    if need_update_timestamp:
        instance.last_update = datetime.datetime.now()
