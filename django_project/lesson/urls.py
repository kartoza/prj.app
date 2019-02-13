# coding=utf-8
"""Urls for lesson application."""

from django.conf.urls import patterns, url

from django.conf import settings

from lesson.views.answer import (
    AnswerCreateView,
    AnswerUpdateView,
    AnswerDeleteView,
)
from lesson.views.question import (
    QuestionCreateView,
    QuestionDeleteView,
    QuestionUpdateView,
    QuestionOrderView,
    QuestionOrderSubmitView,
)
from lesson.views.further_reading import (
    FurtherReadingCreateView,
    FurtherReadingDeleteView,
    FurtherReadingUpdateView,
)
from lesson.views.section import (
    SectionCreateView,
    SectionListView,
    SectionDeleteView,
    SectionUpdateView,
    SectionOrderView,
    AboutLessonsApp,
    SectionOrderSubmitView,
)
from lesson.views.worksheet import (
    WorksheetCreateView,
    WorksheetUpdateView,
    WorksheetDeleteView,
    WorksheetDetailView,
    WorksheetPrintView,
    WorksheetOrderView,
    WorksheetOrderSubmitView,
    WorksheetModuleQuestionAnswers,
    WorksheetPDFZipView,
    download_multiple_worksheet
)
from lesson.views.specification import (
    SpecificationCreateView,
    SpecificationOrderView,
    SpecificationOrderSubmitView,
    SpecificationUpdateView,
    SpecificationDeleteView
)

urlpatterns = patterns(
    '',
    url(regex='^(?P<project_slug>[\w-]+)/section/about/$',
        view=AboutLessonsApp.as_view(),
        name='about-lesson-app'),
    # Section
    url(regex='^(?P<project_slug>[\w-]+)/section/create/$',
        view=SectionCreateView.as_view(),
        name='section-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/list/$',
        view=SectionListView.as_view(),
        name='section-list'),
    url(regex='^(?P<project_slug>[\w-]+)/section/order/$',
        view=SectionOrderView.as_view(),
        name='section-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/submit_order/$',
        view=SectionOrderSubmitView.as_view(),
        name='section-submit-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/(?P<slug>[\w-]+)/update/$',
        view=SectionUpdateView.as_view(),
        name='section-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/(?P<slug>[\w-]+)/delete/$',
        view=SectionDeleteView.as_view(),
        name='section-delete'),

    # Worksheet
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              'download-multiple-worksheet/$',
        view=download_multiple_worksheet,
        name='download-multiple-worksheets'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/create/$',
        view=WorksheetCreateView.as_view(),
        name='worksheet-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/update/(?P<pk>[\w-]+)/$',
        view=WorksheetUpdateView.as_view(),
        name='worksheet-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/delete/(?P<pk>[\w-]+)/$',
        view=WorksheetDeleteView.as_view(),
        name='worksheet-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/detail/(?P<pk>[\w-]+)/$',
        view=WorksheetDetailView.as_view(),
        name='worksheet-detail'),

    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/answers/(?P<pk>[\w-]+)/$',
        view=WorksheetModuleQuestionAnswers.as_view(),
        name='worksheet-module-answers'),

    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/zip/(?P<pk>[\w-]+)/$',
        view=WorksheetPDFZipView.as_view(),
        name='worksheet-zip'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/print/(?P<pk>[\w-]+)/$',
        view=WorksheetPrintView.as_view(),
        name='worksheet-print'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/order$',
        view=WorksheetOrderView.as_view(),
        name='worksheet-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/submit_order/$',
        view=WorksheetOrderSubmitView.as_view(),
        name='worksheet-submit-order'),
    # Specification
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/create/$',
        view=SpecificationCreateView.as_view(),
        name='specification-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/order/$',
        view=SpecificationOrderView.as_view(),
        name='specification-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/submit_order/$',
        view=SpecificationOrderSubmitView.as_view(),
        name='specification-submit-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/'
              'update/(?P<pk>[\w-]+)/$',
        view=SpecificationUpdateView.as_view(),
        name='specification-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/specification/'
              'delete/(?P<pk>[\w-]+)/$',
        view=SpecificationDeleteView.as_view(),
        name='specification-delete'),
    # Further more
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/further-reading/create/$',
        view=FurtherReadingCreateView.as_view(),
        name='further-reading-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/further-reading/'
              'update/(?P<pk>[\w-]+)/$',
        view=FurtherReadingUpdateView.as_view(),
        name='further-reading-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/further-reading/'
              'delete/(?P<pk>[\w-]+)/$',
        view=FurtherReadingDeleteView.as_view(),
        name='further-reading-delete'),
    # Question
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/question/create/$',
        view=QuestionCreateView.as_view(),
        name='question-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/question/'
              'delete/(?P<pk>[\w-]+)/$',
        view=QuestionDeleteView.as_view(),
        name='question-delete'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/question/'
              'update/(?P<pk>[\w-]+)/$',
        view=QuestionUpdateView.as_view(),
        name='question-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/question/order/$',
        view=QuestionOrderView.as_view(),
        name='question-order'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/question/submit_order/$',
        view=QuestionOrderSubmitView.as_view(),
        name='question-submit-order'),
    # Answer
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/question/'
              '(?P<question_pk>[\w-]+)/answer/create$',
        view=AnswerCreateView.as_view(),
        name='answer-create'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/answer/'
              'update/(?P<pk>[\w-]+)/$',
        view=AnswerUpdateView.as_view(),
        name='answer-update'),
    url(regex='^(?P<project_slug>[\w-]+)/section/'
              '(?P<section_slug>[\w-]+)/worksheet/'
              '(?P<worksheet_slug>[\w-]+)/answer/'
              'delete/(?P<pk>[\w-]+)/$',
        view=AnswerDeleteView.as_view(),
        name='answer-delete'),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
