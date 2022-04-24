from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.db.models import Max
from django.urls import reverse
from django.views.generic import CreateView

from base.models import Project
from certification.models.checklist import Checklist


class CertificateChecklistForm(forms.ModelForm):

    class Meta:
        model = Checklist
        fields = (
            'question',
            'show_text_box',
            'help_text',
            'target',
            'project'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        self.helper = FormHelper()

        self.helper.html5_required = False
        super(CertificateChecklistForm, self).__init__(*args, **kwargs)
        self.fields['project'].initial = self.project
        self.fields['project'].widget = forms.HiddenInput()
        self.fields['target'].required = True

    def save(self, commit=True):
        instance = super(CertificateChecklistForm, self).save(commit=False)

        # Update order
        max_order = Checklist.objects.filter(
            project=self.project
        ).aggregate(Max('order'))
        instance.approved = True
        if isinstance(max_order['order__max'], int):
            instance.order = max_order['order__max'] + 1

        instance.save()
        return instance


class CertificateChecklistCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create view for checklist."""

    model = Checklist
    form_class = CertificateChecklistForm
    project = None

    context_object_name = 'checklist'
    template_name = 'certificate_checklist/create.html'

    def test_func(self):
        project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=project_slug)
        return self.project.certification_managers.filter(
            id=self.request.user.id
        ).exists() or self.request.user.is_superuser

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Certification management page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('certification-management-view', kwargs={
            'project_slug': self.project_slug
        })

    def get_context_data(self, **kwargs):
        ctx = super(
            CertificateChecklistCreateView, self
        ).get_context_data(**kwargs)
        ctx['project'] = self.project
        return ctx

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(CertificateChecklistCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.project = Project.objects.get(slug=self.project_slug)
        kwargs.update({
            'user': self.request.user,
            'project': self.project
        })
        return kwargs
