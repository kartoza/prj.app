# coding=utf-8
from django.http import Http404
from django.views.generic import DetailView
from ..models import Certificate


class CertificateDetailView(DetailView):
    """Detail view for Certificate."""

    model = Certificate
    context_object_name = 'certificate'
    template_name = 'certificate/detail.html'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        self.certificateID = self.kwargs.get('id', None)
        context = super(
            CertificateDetailView, self).get_context_data(**kwargs)
        context['certificate'] = \
            Certificate.objects.get(certificateID=self.certificateID)
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: Queryset which is all certificate in the
            corresponding organisation.
        :rtype: QuerySet
        """

        qs = Certificate.objects.all()
        return qs

    def get_object(self, queryset=None):
        """Get the object for this view.

        :param queryset: A query set
        :type queryset: QuerySet

        :returns: Queryset which is filtered to only show a course type
            within the organisation.
        :rtype: QuerySet
        :raises: Http404
        """

        if queryset is None:
            queryset = self.get_queryset()
            certificateID = self.kwargs.get('id', None)
            if certificateID:
                obj = queryset.get(
                    certificateID=certificateID)
                return obj
            else:
                raise Http404('Sorry! Certificate by this ID is not exist.')
