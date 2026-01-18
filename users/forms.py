from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form that uses email as the unique identifier
    instead of username. Includes custom validations and Portuguese help texts.
    """

    email = forms.EmailField(
        label='E-mail',
        help_text='Digite seu endereço de e-mail',
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-gray-700 border border-gray-600 text-gray-100 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'seu@email.com'
        })
    )

    password1 = forms.CharField(
        label='Senha',
        help_text='Sua senha deve conter pelo menos 8 caracteres e não pode ser muito comum',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-700 border border-gray-600 text-gray-100 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': '••••••••'
        })
    )

    password2 = forms.CharField(
        label='Confirme a senha',
        help_text='Digite a mesma senha novamente para confirmação',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-gray-700 border border-gray-600 text-gray-100 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': '••••••••'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        """
        Validate that the email is unique in the database.

        Returns:
            str: The cleaned and normalized email

        Raises:
            ValidationError: If the email already exists
        """
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError(
                'Este e-mail já está cadastrado. Por favor, use outro endereço de e-mail.'
            )
        return email.lower()

    def clean_password2(self):
        """
        Validate that the two password entries match.

        Returns:
            str: The validated password

        Raises:
            ValidationError: If passwords don't match
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('As senhas não coincidem. Por favor, tente novamente.')

        return password2

    def save(self, commit=True):
        """
        Save the user instance with the provided email and password.

        Args:
            commit: Whether to save the instance to the database

        Returns:
            CustomUser: The created user instance
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        if commit:
            user.save()
        return user
