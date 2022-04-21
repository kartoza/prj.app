import re

from braces.views import UserPassesTestMixin
from django.contrib.sessions.backends.db import SessionStore
from django.http.response import Http404
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
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not re.fullmatch(regex, email):
            raise Http404('Invalid email address')

        external_reviewer, created = ExternalReviewer.objects.get_or_create(
            email=email,
            certifying_organisation=self.certifying_organisation
        )

        if created:
            # Create new session
            s = SessionStore()
            s['email'] = email
            s['external_reviewer'] = external_reviewer.id
            s.create()

            external_reviewer.session_key = s.session_key
            external_reviewer.save()

        return Response({
            'created': created
        })
