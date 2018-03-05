# coding=utf-8
"""Translation for lesson app."""

from modeltranslation.translator import translator, TranslationOptions

from lesson.models.answer import Answer
from lesson.models.further_reading import FurtherReading
from lesson.models.section import Section
from lesson.models.specification import Specification
from lesson.models.worksheet import Worksheet
from lesson.models.worksheet_question import WorksheetQuestion


class AnswerTranslation(TranslationOptions):
    fields = ('answer', 'answer_explanation')


class FurtherReadingTranslation(TranslationOptions):
    fields = ('text', )


class SectionTranslation(TranslationOptions):
    fields = ('name', 'notes')


class SpecificationTranslation(TranslationOptions):
    fields = ('title', 'value', 'notes')


class WorksheetTranslation(TranslationOptions):
    fields = (
        'module',
        'title',
        'summary_leader',
        'summary_text',
        'exercise_goal',
        'exercise_task',
        'more_about_text',
        'last_update',
    )


class WorksheetQuestionTranslation(TranslationOptions):
    fields = ('question', )


translator.register(Answer, AnswerTranslation)
translator.register(FurtherReading, FurtherReadingTranslation)
translator.register(Section, SectionTranslation)
translator.register(Specification, SpecificationTranslation)
translator.register(Worksheet, WorksheetTranslation)
translator.register(WorksheetQuestion, WorksheetQuestionTranslation)
