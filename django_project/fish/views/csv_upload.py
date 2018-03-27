# coding=utf-8
"""CSV uploader view
"""

from django.urls import reverse_lazy
from django.views.generic import FormView
from fish.forms.csv_upload import CsvUploadForm


class CsvUploadView(FormView):
    """Csv upload view."""

    form_class = CsvUploadForm
    template_name = 'csv_uploader.html'
    context_data = dict()
    success_url = reverse_lazy('csv-upload')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['data'] = self.context_data
        self.context_data = dict()
        return self.render_to_response(context)

    def form_valid(self, form):
        form.save(commit=True)
        self.context_data['uploaded'] = 'success'
        return super(CsvUploadView, self).form_valid(form)
