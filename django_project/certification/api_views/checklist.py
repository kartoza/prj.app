
from braces.views import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from certification.models.checklist import Checklist


class UpdateChecklistReviewer(LoginRequiredMixin, APIView):
    """API for updating checklist submitted by organization reviewer."""

    def post(self, request, project_slug):
        post_data = request.POST.dict()
        # Checklist data
        cleaned_data = {}
        for key, value in post_data.items():
            checklist_id = None
            if 'checklist-' in key:
                checklist_id = key.split('-')[1]
                if checklist_id not in cleaned_data:
                    cleaned_data[checklist_id] = {
                        'selected': value
                    }
                else:
                    cleaned_data[checklist_id]['selected'] = (
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
        return Response(cleaned_data)
