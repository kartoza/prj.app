# coding=utf-8
from django.http import Http404
from django.urls import reverse
from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.models import User
from ..forms import UserForm


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'account/update.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template.

        :param kwargs: Any arguments to pass to the superclass.
        :type kwargs: dict

        :returns: Context data which will be passed to the template.
        :rtype: dict
        """

        context = super(
            UserUpdateView, self).get_context_data(**kwargs)

        # Only the user itself can update their profile.
        if self.request.user.pk != context['user'].pk:
            raise Http404
        return context

    def get_queryset(self):
        """Get the queryset for this view.

        :returns: All Course Convener objects
        :rtype: QuerySet
        """

        qs = User.objects.all()
        return qs

    def get_form_kwargs(self):
        """Get keyword arguments from form.

        :returns keyword argument from the form
        :rtype: dict
        """

        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

    def get_success_url(self):
        """Define the redirect URL.

        After successful update of the object, the user will be redirected to
        the user profile page.

        :returns: URL
        :rtype: HttpResponse
        """

        return reverse('user-profile')
