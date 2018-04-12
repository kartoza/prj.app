# coding=utf-8

from django.urls import path
from django.views.generic import TemplateView
from geocontext.urls import urlpatterns as geocontext_urls

urlpatterns = [
    path('', TemplateView.as_view(template_name="landing_page.html")),
] + geocontext_urls
