# coding=utf-8
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.views.generic import CreateView, DetailView
from base.models.project import Project
from base.views.certificate_preview import generate_certificate_pdf
from certification.models.certifying_organisation import CertifyingOrganisation
from certification.models.organisation_certificate import \
    CertifyingOrganisationCertificate
from certification.forms import OrganisationCertificateForm


class OrganisationCertificateCreateView(LoginRequiredMixin, CreateView):
    """Create view for Certificate for Certifying Organisation."""

    model = CertifyingOrganisationCertificate
    form_class = OrganisationCertificateForm
    context_object_name = 'certificate'
    template_name = 'certificate_organisation/create.html'

    def get_success_url(self):
        """Define the redirect URL.

        After successful creation of the object, the User will be redirected
        to the Course detail page.

       :returns: URL
       :rtype: HttpResponse
       """

        return reverse('certifyingorganisation-list', kwargs={
            'project_slug': self.project_slug,
        })

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            OrganisationCertificateCreateView, self).get_context_data(**kwargs)
        context['certifying_organisation'] = self.certifying_organisation
        return context

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(
            OrganisationCertificateCreateView, self).get_form_kwargs()
        self.project_slug = self.kwargs.get('project_slug', None)
        self.organisation_slug = self.kwargs.get('organisation_slug', None)
        self.certifying_organisation = \
            CertifyingOrganisation.objects.get(slug=self.organisation_slug)
        kwargs.update({
            'user': self.request.user,
            'certifying_organisation': self.certifying_organisation
        })
        return kwargs


def organisation_certificate_pdf_view(request, **kwargs):
    project_slug = kwargs.pop('project_slug')
    organisation_slug = kwargs.pop('organisation_slug')
    project = Project.objects.get(slug=project_slug)
    certifying_organisation = \
        CertifyingOrganisation.objects.get(slug=organisation_slug)
    certificate = \
        CertifyingOrganisationCertificate.objects.get(
            certifying_organisation=certifying_organisation
        )
    current_site = request.META['HTTP_HOST']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = \
        'filename="{}.pdf"'.format(certificate.certificateID)

    generate_certificate_pdf(
        pathname=response,
        certificate=certificate,
        project=project,
        certifying_organisation=certifying_organisation,
        current_site=current_site
    )

    return response


class OrganisationCertificateDetailView(DetailView):
    """Detail view for Certificate."""

    model = CertifyingOrganisationCertificate
    context_object_name = 'certificate'
    template_name = 'certificate_organisation/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.certificateID = self.kwargs.get('id', None)
        self.project_slug = self.kwargs.get('project_slug', None)
        context = super(
            OrganisationCertificateDetailView, self).get_context_data(**kwargs)
        context['project_slug'] = self.project_slug
        context['history'] = \
            context['certificate'].history.all().order_by('history_date')

        if self.project_slug:
            context['the_project'] = \
                Project.objects.get(slug=self.project_slug)
            context['project'] = context['the_project']
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all certificate in the
            corresponding project.
        :rtype: QuerySet
        """

        qs = CertifyingOrganisationCertificate.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a certificate
            depends on the input certificate ID.
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            certificateID = self.kwargs.get('id', None)
            if certificateID:
                try:
                    obj = queryset.get(certificateID=certificateID)
                    return obj
                except CertifyingOrganisationCertificate.DoesNotExist:
                    return None
            else:
                raise Http404('Sorry! Certificate by this ID does not exist.')

