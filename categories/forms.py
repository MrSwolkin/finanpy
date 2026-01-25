from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    """
    Form for creating and editing transaction categories.
    Includes color picker, custom styling with TailwindCSS, and Portuguese labels.
    Prevents editing of default categories.
    """

    class Meta:
        model = Category
        fields = ['name', 'category_type', 'color']
        labels = {
            'name': 'Nome da Categoria',
            'category_type': 'Tipo',
            'color': 'Cor',
        }
        help_texts = {
            'name': 'Digite um nome descritivo para a categoria',
            'category_type': 'Selecione se é uma receita ou despesa',
            'color': 'Escolha uma cor para identificar a categoria',
        }
        error_messages = {
            'name': {
                'required': 'O nome da categoria é obrigatório',
                'max_length': 'O nome da categoria deve ter no máximo 100 caracteres',
            },
            'category_type': {
                'required': 'O tipo de categoria é obrigatório',
                'invalid_choice': 'Selecione um tipo de categoria válido',
            },
            'color': {
                'required': 'A cor da categoria é obrigatória',
                'max_length': 'A cor deve estar no formato hexadecimal (ex: #6b7280)',
            },
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ex: Salário, Alimentação, Transporte',
                'data-validate': 'true',
                'data-required': 'true',
                'aria-describedby': 'id_name_help',
                'aria-required': 'true'
            }),
            'category_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'aria-describedby': 'id_category_type_help',
                'aria-required': 'true'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-12 px-2 py-1 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'value': '#6b7280',
                'aria-describedby': 'id_color_help',
                'aria-required': 'true'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and store the user for validation.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If editing an existing category, check if it's a default category
        if self.instance and self.instance.pk and self.instance.is_default:
            # Disable all fields for default categories
            for field_name in self.fields:
                self.fields[field_name].disabled = True
                self.fields[field_name].help_text = 'Categorias padrão não podem ser editadas'

    def clean_name(self):
        """
        Custom validation for name field.
        Ensures the name is unique per user and not empty.
        """
        name = self.cleaned_data.get('name')

        if not name or not name.strip():
            raise forms.ValidationError('O nome da categoria é obrigatório')

        name = name.strip()

        # Check if we're editing an existing category
        if self.instance and self.instance.pk:
            # If editing, exclude the current instance from uniqueness check
            if self.user and Category.objects.filter(
                user=self.user,
                name__iexact=name
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Você já possui uma categoria com este nome. '
                    'Escolha um nome diferente.'
                )
        else:
            # If creating new, check if name already exists for this user
            if self.user and Category.objects.filter(
                user=self.user,
                name__iexact=name
            ).exists():
                raise forms.ValidationError(
                    'Você já possui uma categoria com este nome. '
                    'Escolha um nome diferente.'
                )

        return name

    def clean_color(self):
        """
        Custom validation for color field.
        Ensures the color is in valid hexadecimal format.
        """
        color = self.cleaned_data.get('color')

        if not color:
            raise forms.ValidationError('A cor da categoria é obrigatória')

        # Ensure color starts with # and is 7 characters long (#RRGGBB)
        if not color.startswith('#') or len(color) != 7:
            raise forms.ValidationError(
                'A cor deve estar no formato hexadecimal (ex: #6b7280)'
            )

        # Validate hexadecimal characters
        try:
            int(color[1:], 16)
        except ValueError:
            raise forms.ValidationError(
                'A cor deve conter apenas caracteres hexadecimais válidos'
            )

        return color.lower()

    def clean(self):
        """
        Global form validation.
        Prevents editing of default categories.
        """
        cleaned_data = super().clean()

        # Check if trying to edit a default category
        if self.instance and self.instance.pk and self.instance.is_default:
            raise forms.ValidationError(
                'Categorias padrão não podem ser editadas. '
                'Crie uma nova categoria personalizada se desejar.'
            )

        return cleaned_data
