from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm
from .models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Display the current user's profile information.
    Users can only view their own profile.
    """
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """Return the profile of the currently logged-in user."""
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update the current user's profile information.
    Users can only edit their own profile.
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = reverse_lazy('profiles:detail')
    success_message = 'Perfil atualizado com sucesso!'

    def get_object(self, queryset=None):
        """Return the profile of the currently logged-in user."""
        return self.request.user.profile
