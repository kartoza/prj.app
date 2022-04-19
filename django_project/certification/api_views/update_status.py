# coding=utf-8
from braces.views import LoginRequiredMixin
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView, Response
from ..models.certifying_organisation import CertifyingOrganisation
from ..models.status import Status
from ..views import send_rejection_email, send_approved_email


class UpdateStatusOrganisation(LoginRequiredMixin, APIView):
    """API to update the status of an organisation."""

    def post(self, request, project_slug, slug):
        try:
            certifyingorganisation = (
                CertifyingOrganisation.objects.get(slug=slug)
            )
            status_id = request.POST.get('status', None)
            remarks = request.POST.get('remarks', '')
            certifyingorganisation.remarks = remarks
            status_name = None

            if status_id:
                try:
                    status_qs = Status.objects.get(id=status_id)
                    certifyingorganisation.status = status_qs
                    status_name = status_qs.name.lower()

                    site = request.get_host()

                    if status_name == 'approved':
                        certifyingorganisation.approved = True

                        send_approved_email(
                            certifyingorganisation,
                            site
                        )

                    elif status_name == 'rejected':
                        certifyingorganisation.rejected = True

                        schema = request.is_secure() and "https" or "http"

                        send_rejection_email(
                            certifyingorganisation,
                            site,
                            schema
                        )

                    certifyingorganisation.owner_message = ''
                except Status.DoesNotExist:
                    return HttpResponse(
                        'Status object does not exist.',
                        status=status.HTTP_400_BAD_REQUEST
                    )

            certifyingorganisation.save()
            return Response({
                'success': True,
                'status': status_name
            })

        except CertifyingOrganisation.DoesNotExist:
            return HttpResponse(
                'Certifying Organisation does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )
