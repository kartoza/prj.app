from rest_framework import serializers

from certification.models import Checklist, OrganisationChecklist


class OrganisationChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationChecklist
        fields = ['checked', 'text_box_content', 'checklist_question']


class ChecklistSerializer(serializers.ModelSerializer):

    organisation_checklist = OrganisationChecklistSerializer(
        source='organisationchecklist_set', many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = [
            'id', 'question', 'show_text_box',
            'target', 'organisation_checklist',
            'help_text']
