from braces.views import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    RedirectView)
from django import forms
from django.http.response import HttpResponse
from changes.models import Sponsor
from base.models import Project


class SustainingMemberForm(forms.ModelForm):
    class Meta:
        """Meta class."""
        model = Sponsor
        fields = (
            'name',
            'contact_title',
            'sponsor_url',
            'contact_person',
            'address',
            'country',
            'sponsor_email',
            'agreement',
            'logo',
        )


class SustainingMemberCreateView(LoginRequiredMixin, CreateView):
    """Create view for sustaining member"""
    template_name = 'sustaining_member/add.html'
    model = Sponsor
    form_class = SustainingMemberForm
    form_object = None

    def get_success_url(self):
        return reverse('sponsor-list', kwargs={
            'project_slug': self.form_object.project.slug
        })

    def form_valid(self, form):
        """Check if form is valid."""
        if form.is_valid():
            self.form_object = form.save(commit=False)
            self.form_object.author = self.request.user
            self.form_object.project = Project.objects.get(
                slug=self.kwargs.get('project_slug')
            )
            self.form_object.save()
            return super(SustainingMemberCreateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SustainingMemberDetailView(LoginRequiredMixin, DetailView):
    """Detail view for sustaining member"""
    def get(self, request, *args, **kwargs):
        user = self.request.user
        try:
            sponsor = Sponsor.objects.get(
                author=user
            )
        except Sponsor.DoesNotExist:
            pass
        return HttpResponse('ok')
