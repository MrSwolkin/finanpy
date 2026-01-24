from decimal import Decimal
from django import forms
from .models import Account


class AccountForm(forms.ModelForm):
    """
    Form for creating and editing bank accounts.
    Includes custom styling with TailwindCSS and Portuguese labels.
    """

    class Meta:
        model = Account
        fields = ['name', 'account_type', 'initial_balance']
        labels = {
            'name': 'Nome da Conta',
            'account_type': 'Tipo de Conta',
            'initial_balance': 'Saldo Inicial',
        }
        help_texts = {
            'name': 'Digite um nome descritivo para identificar sua conta',
            'account_type': 'Selecione o tipo de conta bancária',
            'initial_balance': 'Informe o saldo inicial da conta (pode ser negativo)',
        }
        error_messages = {
            'name': {
                'required': 'O nome da conta é obrigatório',
                'max_length': 'O nome da conta deve ter no máximo 100 caracteres',
            },
            'account_type': {
                'required': 'O tipo de conta é obrigatório',
                'invalid_choice': 'Selecione um tipo de conta válido',
            },
            'initial_balance': {
                'required': 'O saldo inicial é obrigatório',
                'invalid': 'Digite um valor numérico válido',
                'max_digits': 'O valor deve ter no máximo 12 dígitos',
                'max_decimal_places': 'O valor deve ter no máximo 2 casas decimais',
            },
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ex: Banco do Brasil - Conta Corrente',
                'data-validate': 'true',
                'data-required': 'true',
            }),
            'account_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            }),
            'initial_balance': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': '0,00',
                'step': '0.01',
            }),
        }

    def clean_name(self):
        """
        Custom validation for name field.
        Ensures the name is required and not empty.
        """
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise forms.ValidationError('O nome da conta é obrigatório')
        return name.strip()

    def clean_initial_balance(self):
        """
        Custom validation for initial_balance field.
        Allows negative values (overdraft/debt situations).
        """
        initial_balance = self.cleaned_data.get('initial_balance')

        if initial_balance is None:
            raise forms.ValidationError('O saldo inicial é obrigatório')

        # Explicitly allow negative values (no validation error for negative amounts)
        # This allows users to start with debt/overdraft

        return initial_balance

    def save(self, commit=True):
        """
        Override save method to set current_balance equal to initial_balance
        when creating a new account.
        """
        account = super().save(commit=False)

        # For new accounts, set current_balance to initial_balance
        if not account.pk:
            account.current_balance = account.initial_balance

        if commit:
            account.save()

        return account
