import re

from braces.views import UserPassesTestMixin
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
from django.http.response import Http404
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from certification.models import CertifyingOrganisation, ExternalReviewer


class InviteReviewerApiView(UserPassesTestMixin, APIView):
    """Api to invite external reviewer"""
    certifying_organisation = None

    def test_func(self, user):

        try:
            self.certifying_organisation = (
                CertifyingOrganisation.objects.get(
                    slug=self.kwargs.get('slug', None))
            )
        except CertifyingOrganisation.DoesNotExist:
            return False
        if (
                user.is_staff or
                user in self.certifying_organisation.project.
                certification_managers.all() or
                user == self.certifying_organisation.project.owner):
            return True

        return False

    def post(self, request, project_slug, slug):
        email = request.POST.get('email', None)
        name = request.POST.get('name')
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not re.fullmatch(regex, email):
            raise Http404('Invalid email address')

        external_reviewer, created = ExternalReviewer.objects.get_or_create(
            name=name,
            email=email,
            certifying_organisation=self.certifying_organisation
        )

        if created:
            # Create new session
            s = SessionStore()
            s['email'] = email
            s['external_reviewer'] = external_reviewer.id
            s.create()

            # Send email
            site = request.get_host()
            schema = request.is_secure() and "https" or "http"

            data = {
                'name': name,
                'email': email,
                'invitation_text': (
                    self.certifying_organisation.project.
                    external_reviewer_invitation
                ),
                'organisation_name': self.certifying_organisation.name,
                'project_name': self.certifying_organisation.project.name,
                'project_owner_firstname':
                    self.certifying_organisation.project.owner.first_name,
                'project_owner_lastname':
                    self.certifying_organisation.project.owner.last_name,
                'site': site,
                'project_slug': self.certifying_organisation.project.slug,
                'slug': self.certifying_organisation.slug,
                'schema': schema,
                'session_key': s.session_key
            }
            send_mail(
                u'Changelog - You have been invited as a reviewer',
                u'Dear {name},\n\n'
                u'{invitation_text}'
                u'\n\n'
                u'Detail organisation :\n'
                u'Name of organisation: {organisation_name}\n'
                u'Project: {project_name}\n'
                u'\n\n'
                u'To review the organisation please follow this link: '
                u'{schema}://{site}/en/{project_slug}/'
                u'certifyingorganisation/{slug}/?s={session_key}\n\n'
                u'Sincerely,\n'
                u'{project_owner_firstname} {project_owner_lastname}'.format(
                    **data),
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            external_reviewer.session_key = s.session_key
            external_reviewer.save()

        return Response({
            'created': created
        })
