# coding=utf-8

from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', TemplateView.as_view(template_name="landing_page.html")),
    url(r'^api/docs/', include_docs_urls(title='Healthyrivers API'))
]
