# coding=utf-8
# flake8: noqa
"""
core.custom_middleware
"""
from django.contrib.flatpages.models import FlatPage
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import activate
try:
    from django.utils.deprecation import MiddlewareMixin as MiddlewareBase
except ImportError:  # Django < 1.10
    MiddlewareBase = object

from base.models import Project, Version, Domain, ProjectFlatpage
from changes.models import (
    SponsorshipLevel, SponsorshipPeriod, Sponsor
)
from certification.models import CertifyingOrganisation


class NavContextMiddleware(MiddlewareBase):
    """
    Adds the required navigation variables to each response
    """
    def process_template_response(self, request, response):
        """
        Add 'the_project', 'the_entry', 'the_version' to context for the
            navigation.

        Justification: To make the navigation functional, we need to know
            which Project (or Version, Committee etc) the current context
            relates to. This is required for URLs. Rather than include lots of
            if/else in the navigation template, it seems cleaner to add the
            above variables to the context here.

        :param request: Http Request obj
        :param response: Http Response obj
        :return: context :rtype: dict
        """
        context = response.context_data
        if not context:
            return response

        if context.get('project', None):
            context['the_project'] = context.get('project')
            versions = Version.objects.filter(project=context.get('project'))
            context['has_pending_sponsor_lvl'] = (
                SponsorshipLevel.unapproved_objects.filter(
                    project=context.get('project')).exists())
            context['has_pending_sponsor_period'] = (
                SponsorshipPeriod.unapproved_objects.filter(
                    project=context.get('project')).exists())
            context['has_pending_organisations'] = (
                CertifyingOrganisation.unapproved_objects.filter(
                    project=context.get('project')).exists())

            # Check if user is a sustaining member manager
            if request.user.is_anonymous:
                context['has_pending_sustaining_members'] = False
            else:
                context['has_pending_sustaining_members'] = (
                    Sponsor.unapproved_objects.filter(
                        project=context.get('project'),
                        project__sponsorship_managers__in=[request.user]
                    ).exists()
                )
            context['project_flatpages'] = ProjectFlatpage.objects.filter(
                project=context['the_project']
            )

        else:
            if request.user.is_staff:
                context['the_projects'] = Project.objects.all()
            else:
                context['the_projects'] = Project.approved_objects.filter(
                    private=False
                )

        if context.get('version', None):
            context['the_version'] = context.get('version')
            context['the_project'] = context.get('version').project

        if context.get('committee', None):
            context['the_committee'] = context.get('committee')
            context['the_project'] = context.get('committee').project

        if context.get('ballot', None):
            context['the_committee'] = context.get('ballot').committee
            context['the_project'] = context.get('ballot').committee.project

        if context.get('category', None):
            context['the_project'] = context.get('category').project

        if context.get('ballots', None):
            try:
                context['the_project'] = \
                    context.get('ballots')[0].committee.project
            except (KeyError, IndexError):
                pass

        if context.get('entry', None):
            context['the_entry'] = context.get('entry')
            context['the_version'] = context.get('entry').version
            context['the_project'] = context.get('entry').version.project

        if context.get('committees', None):
            try:
                context['the_project'] = context.get('committees')[0].project
            except (KeyError, IndexError):
                pass

        if context.get('versions', None):
            try:
                context['the_project'] = context.get('versions')[0].project
            except (KeyError, IndexError):
                pass

        if context.get('entries', None):
            try:
                context['the_version'] = context.get('entries')[0].version
                context['the_project'] = \
                    context.get('entries')[0].version.project
            except (KeyError, IndexError):
                pass

        if context.get('categories', None):
            try:
                context['the_project'] = \
                    context.get('categories')[0].project
            except (KeyError, IndexError):
                pass

        project_flatpage_ids = (
            ProjectFlatpage.objects.all().values_list('id', flat=True))
        context['flatpages'] = (
            FlatPage.objects.exclude(id__in=project_flatpage_ids))

        return response


class CheckDomainMiddleware(MiddlewareBase):
    """
    Custom middleware to check if domain is valid.
    """
    def process_request(self, request):
        try:
            domain = request.get_host().split(':')[0]
            if domain in settings.VALID_DOMAIN:
                return None
            else:
                custom_domain = Domain.objects.get(
                    domain=domain, approved=True)
                request.site = custom_domain.domain
                activate('en')
                url = reverse('project-list')
                home_url = reverse('home')
                if custom_domain.role == 'Project':
                    # Get current project path
                    try:
                        project_url_path = request.path.split(home_url)[1]
                    except IndexError:
                        project_url_path = '/'
                    project_url_path = project_url_path.split('/')[0]
                    is_different_project = (
                        Project.objects.filter(
                            name__iexact=project_url_path
                        ).exclude(id=custom_domain.project.id).exists()
                    )

                    if (
                            request.path == url or
                            request.path == home_url or
                            project_url_path == '' or
                            is_different_project):
                        return redirect(
                            'project-detail', custom_domain.project.slug)
                elif custom_domain.role == 'Organisation':
                    return None
        except Domain.DoesNotExist:
            if not settings.DEBUG:
                # for production the domain is hardcoded for consistency
                return HttpResponseRedirect(
                    'http://changelog.kartoza.com/en/domain-not-found/'
                )
