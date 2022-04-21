from django.urls import reverse

from django.shortcuts import redirect

from certification.models import CertifyingOrganisation
from certification.models.checklist import Checklist
from certification.models.organisation_checklist import OrganisationChecklist
from certification.views import CertifyingOrganisationUserTestMixin


class UpdateChecklistReviewer(CertifyingOrganisationUserTestMixin):
    """
    API for submitting new checklist or updating existing one
    that was done by reviewer.
    """

    def post(self, request, project_slug, slug):
        post_data = request.POST.dict()
        organisation = CertifyingOrganisation.objects.get(
            slug=slug
        )
        cleaned_data = {}
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
                        True if value == 'yes' else False
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
                    del cleaned_data[checklist_id]
                    continue
                cleaned_data[checklist_id]['question'] = (
                    checklist.question
                )

        for key, value in cleaned_data.items():
            checklist = Checklist.objects.get(id=key)
            org_checklist, created = (
                OrganisationChecklist.objects.get_or_create(
                    organisation=organisation,
                    checklist=checklist
                )
            )
            if created:
                if not self.request.user.is_anonymous:
                    org_checklist.submitter = self.request.user
                elif self.external_reviewer:
                    org_checklist.external_submitter = (
                        self.external_reviewer
                    )
                org_checklist.checklist_question = value['question']
                org_checklist.checklist_target = checklist.target

            if 'checked' in value:
                org_checklist.checked = value['checked']
            if 'text' in value:
                org_checklist.text_box_content = value['text']

            org_checklist.save()

        if organisation:
            change_reason = 'Checklist updated by {}'
            if self.external_reviewer:
                change_reason = change_reason.format(
                    f'external reviewer '
                    f'({self.external_reviewer.email})'
                )
            else:
                change_reason = change_reason.format(
                    self.request.user.username
                )
            organisation._change_reason = (
                change_reason
            )
            organisation.save()

            redirect_url = reverse('certifyingorganisation-detail', kwargs={
                'project_slug': organisation.project.slug,
                'slug': organisation.slug
            })

            if self.external_reviewer:
                redirect_url += f'?s={self.external_reviewer.session_key}'

        return redirect(redirect_url)
