# coding=UTF-8
"""Model admin class definitions."""

from django.contrib import admin
from lesson.models.answer import Answer
from lesson.models.further_reading import FurtherReading
from lesson.models.section import Section
from lesson.models.specification import Specification
from lesson.models.worksheet import Worksheet
from lesson.models.worksheet_question import WorksheetQuestion


class AnswerAdmin(admin.ModelAdmin):
    """Answer admin model."""
    list_display = (
        'question', 'sequence_number', 'answer', 'is_correct',
        'answer_explanation')
    fields = (
        'question', 'answer', 'is_correct', 'answer_explanation')


class FurtherReadingAdmin(admin.ModelAdmin):
    """Further reading admin model."""
    list_display = ('worksheet', 'text', 'link')
    fields = ('worksheet', 'text', 'link')


class SectionAdmin(admin.ModelAdmin):
    """Section admin model."""
    list_display = ('project', 'sequence_number', 'name', 'notes')
    fields = ('project', 'name', 'notes')


class SpecificationAdmin(admin.ModelAdmin):
    """Specification admin model."""
    list_display = (
        'worksheet', 'sequence_number', 'title', 'value', 'notes')
    fields = ('worksheet', 'title', 'value', 'notes')


class WorksheetAdmin(admin.ModelAdmin):
    """Worksheet admin model."""
    list_display = (
        'section', 'sequence_number', 'module', 'title', 'summary_leader',
        'summary_text', 'summary_image', 'exercise_goal', 'exercise_task',
        'more_about_title', 'more_about_text', 'more_about_image',
        'external_data', 'youtube_link', 'author_name', 'author_link'
    )
    fields = (
        'section', 'module', 'title', 'summary_leader',
        'summary_text', 'summary_image', 'exercise_goal', 'exercise_task',
        'more_about_title', 'more_about_text', 'more_about_image',
        'external_data', 'youtube_link', 'author_name', 'author_link'
    )


class WorksheetQuestionAdmin(admin.ModelAdmin):
    """Worksheet question admin model."""
    list_display = (
        'worksheet', 'question', 'sequence_number', 'question_image')
    fields = ('worksheet', 'question', 'question_image')


admin.site.register(Answer, AnswerAdmin)
admin.site.register(FurtherReading, FurtherReadingAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Worksheet, WorksheetAdmin)
admin.site.register(WorksheetQuestion, WorksheetQuestionAdmin)
