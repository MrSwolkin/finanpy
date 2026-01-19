from decimal import Decimal
from django import forms
from .models import Transaction
from accounts.models import Account
from categories.models import Category


class TransactionForm(forms.ModelForm):
    """
    Form for creating and editing transactions.
    Filters accounts and categories by user, includes custom styling with TailwindCSS,
    and Portuguese labels. Adds data attributes to categories for JavaScript filtering by type.
    """

    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'transaction_date', 'transaction_type', 'category', 'account']
        labels = {
            'description': 'Descrição',
            'amount': 'Valor',
            'transaction_date': 'Data da Transação',
            'transaction_type': 'Tipo',
            'category': 'Categoria',
            'account': 'Conta',
        }
        help_texts = {
            'description': 'Digite uma descrição para identificar a transação',
            'amount': 'Informe o valor da transação (apenas valores positivos)',
            'transaction_date': 'Selecione a data em que a transação ocorreu',
            'transaction_type': 'Selecione se é uma receita ou despesa',
            'category': 'Selecione a categoria da transação',
            'account': 'Selecione a conta bancária',
        }
        error_messages = {
            'description': {
                'required': 'A descrição é obrigatória',
                'max_length': 'A descrição deve ter no máximo 255 caracteres',
            },
            'amount': {
                'required': 'O valor é obrigatório',
                'invalid': 'Digite um valor numérico válido',
                'max_digits': 'O valor deve ter no máximo 12 dígitos',
                'max_decimal_places': 'O valor deve ter no máximo 2 casas decimais',
            },
            'transaction_date': {
                'required': 'A data da transação é obrigatória',
                'invalid': 'Digite uma data válida',
            },
            'transaction_type': {
                'required': 'O tipo de transação é obrigatório',
                'invalid_choice': 'Selecione um tipo de transação válido',
            },
            'category': {
                'required': 'A categoria é obrigatória',
                'invalid_choice': 'Selecione uma categoria válida',
            },
            'account': {
                'required': 'A conta é obrigatória',
                'invalid_choice': 'Selecione uma conta válida',
            },
        }
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition duration-200',
                'placeholder': 'Ex: Pagamento de conta de luz',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition duration-200',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0.01',
            }),
            'transaction_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition duration-200',
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition duration-200',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition duration-200',
            }),
            'account': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition duration-200',
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with user parameter.
        Filters accounts and categories by the logged-in user.
        Adds data attributes to category options for JavaScript filtering by type.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            # Filter accounts: only active accounts belonging to the user
            self.fields['account'].queryset = Account.objects.filter(
                user=self.user,
                is_active=True
            ).order_by('name')

            # Filter categories: only categories belonging to the user
            # JavaScript in the template will filter by type dynamically
            self.fields['category'].queryset = Category.objects.filter(
                user=self.user
            ).order_by('category_type', 'name')

            # Add data-type attribute to each category option for JavaScript filtering
            # This allows the template JavaScript to show/hide categories based on transaction_type
            category_choices = []
            for category in self.fields['category'].queryset:
                category_choices.append((category.pk, category.name, category.category_type))

            # Store choices with data attributes
            self._category_choices_with_type = category_choices

    def clean_description(self):
        """
        Custom validation for description field.
        Ensures the description is not empty.
        """
        description = self.cleaned_data.get('description')
        if not description or not description.strip():
            raise forms.ValidationError('A descrição é obrigatória')
        return description.strip()

    def clean_amount(self):
        """
        Custom validation for amount field.
        Ensures the amount is positive (greater than 0).
        """
        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise forms.ValidationError('O valor é obrigatório')

        if amount <= Decimal('0'):
            raise forms.ValidationError(
                'O valor deve ser maior que zero. '
                'Informe apenas valores positivos.'
            )

        return amount

    def clean_category(self):
        """
        Custom validation for category field.
        Ensures the category belongs to the user and matches the transaction type.
        """
        category = self.cleaned_data.get('category')
        transaction_type = self.cleaned_data.get('transaction_type')

        if category and self.user:
            # Verify the category belongs to the user
            if category.user != self.user:
                raise forms.ValidationError('Selecione uma categoria válida')

            # Verify the category type matches the transaction type
            if transaction_type and category.category_type != transaction_type:
                type_label = 'receita' if transaction_type == Transaction.INCOME else 'despesa'
                raise forms.ValidationError(
                    f'A categoria selecionada não é do tipo {type_label}. '
                    f'Selecione uma categoria compatível.'
                )

        return category

    def clean_account(self):
        """
        Custom validation for account field.
        Ensures the account belongs to the user and is active.
        """
        account = self.cleaned_data.get('account')

        if account and self.user:
            # Verify the account belongs to the user
            if account.user != self.user:
                raise forms.ValidationError('Selecione uma conta válida')

            # Verify the account is active
            if not account.is_active:
                raise forms.ValidationError(
                    'A conta selecionada está inativa. '
                    'Selecione uma conta ativa.'
                )

        return account

    def clean(self):
        """
        Global form validation.
        Additional cross-field validation if needed.
        """
        cleaned_data = super().clean()

        # All required fields must be present
        required_fields = ['description', 'amount', 'transaction_date', 'transaction_type', 'category', 'account']
        for field in required_fields:
            if not cleaned_data.get(field):
                # Individual field errors are already raised in field-specific clean methods
                pass

        return cleaned_data
