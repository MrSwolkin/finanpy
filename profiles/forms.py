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

    def clean_avatar(self):
        """
        Validates the uploaded avatar image.
        Checks file size (max 2MB) and format (JPEG, PNG only).
        """
        avatar = self.cleaned_data.get('avatar')

        # If no new file uploaded, return None or existing value
        if not avatar:
            return avatar

        # Validate file size (2MB = 2 * 1024 * 1024 bytes)
        max_size = 2 * 1024 * 1024
        if avatar.size > max_size:
            raise forms.ValidationError(
                'O arquivo é muito grande. O tamanho máximo permitido é 2MB.'
            )

        # Validate file format (JPEG, PNG only)
        allowed_types = ['image/jpeg', 'image/png']
        if avatar.content_type not in allowed_types:
            raise forms.ValidationError(
                'Formato de arquivo não suportado. Use apenas JPG ou PNG.'
            )

        return avatar
