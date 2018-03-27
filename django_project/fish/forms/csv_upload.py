# coding=utf-8
"""Forms to upload csv.
"""

from django import forms
from fish.models.csv_document import CSVDocument


class CsvUploadForm(forms.ModelForm):
    """Csv upload form"""
    class Meta:
        model = CSVDocument
        fields = '__all__'
