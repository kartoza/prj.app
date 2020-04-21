# coding=utf-8
from braces.views import LoginRequiredMixin
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView, Response
from ..models.certifying_organisation import CertifyingOrganisation
from ..models.status import Status


class UpdateStatusOrganisation(LoginRequiredMixin, APIView):
    """API to update the status of an organisation."""

    def post(self, request, project_slug, slug):
        try:
            certifyingorganisation = \
                CertifyingOrganisation.objects.get(slug=slug)
            status_id = request.POST.get('status', None)
            remarks = request.POST.get('remarks', '')
            certifyingorganisation.remarks = remarks

            if status_id:
                try:
                    status_qs = Status.objects.get(id=status_id)
                    certifyingorganisation.status = status_qs

                    if status_qs.name.lower() == 'approved':
                        certifyingorganisation.approved = True
                except Status.DoesNotExist:
                    return HttpResponse(
                        'Status object does not exist.',
                        status=status.HTTP_400_BAD_REQUEST
                    )

            certifyingorganisation.save()
            return Response({'success': True})

        except CertifyingOrganisation.DoesNotExist:
            return HttpResponse(
                'Certifying Organisation does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )
