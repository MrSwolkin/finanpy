from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class SignUpView(SuccessMessageMixin, CreateView):
    """
    View for user registration using email-based authentication.
    Automatically logs in the user after successful registration.
    """

    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Conta criada com sucesso! Bem-vindo ao Finanpy.'

    def form_valid(self, form):
        """
        Handle valid form submission by saving the user and logging them in.

        Args:
            form: The validated CustomUserCreationForm

        Returns:
            HttpResponse: Redirect to the success URL
        """
        response = super().form_valid(form)

        # Log the user in automatically after registration
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')

        return response

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests. Redirect authenticated users to dashboard.

        Returns:
            HttpResponse: Redirect or render the signup form
        """
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """
    Custom login view using email-based authentication.
    Supports the 'next' parameter for redirecting after login.
    """

    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Get the URL to redirect to after successful login.
        Validates the 'next' URL to prevent open redirect attacks.

        Returns:
            str: The URL to redirect to (either validated 'next' parameter or dashboard)
        """
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return reverse_lazy('dashboard')

    def form_valid(self, form):
        """
        Handle valid form submission by logging in the user.

        Args:
            form: The validated authentication form

        Returns:
            HttpResponse: Redirect to the success URL
        """
        response = super().form_valid(form)

        # Add welcome message
        user_email = self.request.user.email
        messages.success(
            self.request,
            f'Bem-vindo de volta! Você está conectado como {user_email}.'
        )

        return response

    def form_invalid(self, form):
        """
        Handle invalid form submission.

        Args:
            form: The invalid authentication form

        Returns:
            HttpResponse: Re-render the form with errors
        """
        messages.error(
            self.request,
            'E-mail ou senha incorretos. Por favor, tente novamente.'
        )
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """
    Custom logout view that redirects to the home page
    and displays a farewell message.
    """

    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        """
        Handle the logout request and add a farewell message.

        Args:
            request: The HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HttpResponse: Redirect to the home page
        """
        if request.user.is_authenticated:
            messages.info(
                request,
                'Você saiu da sua conta com sucesso. Até logo!'
            )

        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    """
    View for requesting a password reset email.
    """

    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        """
        Handle valid form submission. Shows generic message to prevent email enumeration.

        Args:
            form: The validated form

        Returns:
            HttpResponse: Redirect to success page
        """
        messages.info(
            self.request,
            'Se o e-mail informado estiver cadastrado, você receberá instruções para redefinir sua senha.'
        )
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    View displayed after password reset email has been sent.
    """

    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    View for entering a new password after clicking the reset link.
    """

    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        """
        Handle valid form submission by setting the new password.

        Args:
            form: The validated form

        Returns:
            HttpResponse: Redirect to completion page
        """
        messages.success(self.request, 'Sua senha foi alterada com sucesso!')
        return super().form_valid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    View displayed after password has been successfully reset.
    """

    template_name = 'users/password_reset_complete.html'
