# coding=utf-8
"""Factories for creating model instances for testing."""

import factory
import factory.fuzzy
from core.model_factories import UserF
from permission.models import ProjectAdministrator, ProjectCollaborator


class ProjectAdministratorF(factory.django.DjangoModelFactory):
    """
    Category model factory
    """

    class Meta:
        model = ProjectAdministrator

    project = factory.SubFactory('base.tests.model_factories.ProjectF')
    user = factory.SubFactory(UserF)


class ProjectCollaboratorF(factory.django.DjangoModelFactory):
    """
    Category model factory
    """

    class Meta:
        model = ProjectCollaborator

    project = factory.SubFactory('base.tests.model_factories.ProjectF')
    user = factory.SubFactory(UserF)
