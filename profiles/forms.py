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
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'phone': 'Telefone',
            'avatar': 'Foto de Perfil',
        }
        help_texts = {
            'first_name': 'Digite seu primeiro nome',
            'last_name': 'Digite seu sobrenome completo',
            'phone': 'Digite seu telefone no formato (11) 98765-4321',
            'avatar': 'Envie uma foto em formato JPG ou PNG (máximo 2MB)',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Digite seu primeiro nome',
                'aria-describedby': 'id_first_name_help'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Digite seu sobrenome',
                'aria-describedby': 'id_last_name_help'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': '(11) 98765-4321',
                'aria-describedby': 'id_phone_help'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-purple-600 file:text-white hover:file:bg-purple-700',
                'aria-describedby': 'id_avatar_help',
                'accept': 'image/jpeg,image/png'
            }),
        }

    def clean_avatar(self):
        """
        Validates the uploaded avatar image.
        Checks file size (max 2MB) and format (JPEG, PNG only).
        Uses PIL to verify actual file type instead of relying on client-provided content_type.
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

        # Validate real file type with PIL (don't trust client-provided content_type)
        try:
            from PIL import Image
            img = Image.open(avatar)
            img.verify()

            # Reopen after verify
            avatar.seek(0)
            img = Image.open(avatar)

            if img.format.upper() not in ['JPEG', 'PNG']:
                raise forms.ValidationError(
                    'Formato de imagem não suportado. Use JPG ou PNG.'
                )
        except Exception:
            raise forms.ValidationError(
                'Arquivo de imagem inválido ou corrompido.'
            )

        # Reset file pointer
        avatar.seek(0)
        return avatar
