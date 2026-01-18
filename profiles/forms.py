from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    Includes first_name, last_name, phone, and avatar fields with TailwindCSS styling.
    """

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 text-gray-100 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Digite seu primeiro nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 text-gray-100 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Digite seu sobrenome'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 text-gray-100 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': '(11) 98765-4321'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'w-full bg-gray-700 border border-gray-600 text-gray-100 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-purple-600 file:text-white hover:file:bg-purple-700',
            }),
        }
