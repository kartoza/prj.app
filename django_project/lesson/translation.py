# coding=utf-8
"""Translation for lesson app."""

from modeltranslation.translator import TranslationOptions, register

from lesson.models.mixins import TranslationMixin

from lesson.models.answer import Answer
from lesson.models.further_reading import FurtherReading
from lesson.models.license import License
from lesson.models.section import Section
from lesson.models.specification import Specification
from lesson.models.worksheet import Worksheet
from lesson.models.worksheet_question import WorksheetQuestion


@register(TranslationMixin)
class TranslationMixinTranslation(TranslationOptions):
    fields = ('last_update',)


@register(Answer)
class AnswerTranslation(TranslationMixinTranslation):
    fields = ('answer', 'answer_explanation')


@register(FurtherReading)
class FurtherReadingTranslation(TranslationMixinTranslation):
    fields = ('text', )


@register(License)
class LicenseTranslation(TranslationMixinTranslation):
    fields = ('description', )


@register(Section)
class SectionTranslation(TranslationMixinTranslation):
    fields = ('name', 'notes')


@register(Specification)
class SpecificationTranslation(TranslationMixinTranslation):
    fields = ('title', 'value', 'title_notes', 'value_notes')


@register(Worksheet)
class WorksheetTranslation(TranslationMixinTranslation):
    fields = (
        'module',
        'title',
        'summary_leader',
        'summary_text',
        'exercise_goal',
        'exercise_task',
        'more_about_title',
        'more_about_text',
    )


@register(WorksheetQuestion)
class WorksheetQuestionTranslation(TranslationMixinTranslation):
    fields = ('question', )
