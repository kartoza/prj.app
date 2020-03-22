# coding=utf-8
from django.db import models
from django.contrib.flatpages.models import FlatPage
from base.models import Project


class ProjectFlatpage(FlatPage):
    """Extension of Flatpage model to have project property."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
