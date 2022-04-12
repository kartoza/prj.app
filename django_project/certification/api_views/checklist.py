
from braces.views import LoginRequiredMixin
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import redirect

from certification.models import CertifyingOrganisation
from certification.models.checklist import Checklist
from certification.models.organisation_checklist import OrganisationChecklist


class UpdateChecklistReviewer(LoginRequiredMixin, APIView):
    """API for updating checklist submitted by organization reviewer."""

    def post(self, request, project_slug):
        post_data = request.POST.dict()
        organisation_id = post_data.get('organisation', None)
        # Checklist data
        cleaned_data = {}
        organisation = None
        for key, value in post_data.items():
            checklist_id = None
            if 'checklist-' in key:
                checklist_id = key.split('-')[1]
                if checklist_id not in cleaned_data:
                    cleaned_data[checklist_id] = {
                        'checked': True if value == 'yes' else False
                    }
                else:
                    cleaned_data[checklist_id]['checked'] = (
                        value
                    )
            if 'textarea-' in key:
                if not checklist_id:
                    checklist_id = key.split('-')[1]
                if checklist_id not in cleaned_data:
                    cleaned_data[checklist_id] = {
                        'text': value
                    }
                else:
                    cleaned_data[checklist_id]['text'] = (
                        value
                    )
            if checklist_id:
                try:
                    checklist = Checklist.objects.get(
                        id=checklist_id
                    )
                except Checklist.DoesNotExist:
                    continue
                cleaned_data[checklist_id]['question'] = (
                    checklist.question
                )

        for key, value in cleaned_data.items():
            checklist = Checklist.objects.get(id=key)
            organisation = CertifyingOrganisation.objects.get(
                id=organisation_id
            )
            org_checklist, created = OrganisationChecklist.objects.get_or_create(
                organisation=organisation,
                checklist=checklist
            )
            if created:
                org_checklist.submitter = self.request.user
                org_checklist.checklist_question = value['question']
                org_checklist.checklist_target = checklist.target

            org_checklist.checked = value['checked']
            if 'text' in value:
                org_checklist.text_box_content = value['text']

            org_checklist.save()

        if organisation:
            return redirect('certifyingorganisation-detail',
                            project_slug=organisation.project.slug,
                            slug=organisation.slug)
        else:
            return HttpResponse(
                'Organisation does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )
