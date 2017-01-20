from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import edit
from django.contrib.auth import views as auth_views
from django import urls


class UserProfileEdit(LoginRequiredMixin, edit.UpdateView):
    """
    Edit user-editable details about their own profile
    """
    model = User
    fields = [
        'email',
        'username',
    ]
    success_url = urls.reverse_lazy('profile-edit')
    template_name = 'auth/user_form.html'

    def get_object(self, queryset=None):
        """
        Always retrieve the currently logged in user's profile
        """
        if queryset is None:
            queryset = self.get_queryset()

        return self.request.user

