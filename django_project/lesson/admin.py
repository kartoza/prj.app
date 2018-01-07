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


class FurtherReadingAdmin(admin.ModelAdmin):
    """Further reading admin model."""


class SectionAdmin(admin.ModelAdmin):
    """Section admin model."""


class SpecificationAdmin(admin.ModelAdmin):
    """Specification admin model."""

class WorksheetAdmin(admin.ModelAdmin):
    """Worksheet admin model."""

class WorksheetQuestionAdmin(admin.ModelAdmin):
    """Worksheet question admin model."""


admin.site.register(Answer, AnswerAdmin)
admin.site.register(FurtherReading, FurtherReadingAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Worksheet, WorksheetAdmin)
admin.site.register(WorksheetQuestion, WorksheetQuestionAdmin)
