from decimal import Decimal
from datetime import date, timedelta
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
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ex: Pagamento de conta de luz',
                'data-validate': 'true',
                'data-required': 'true',
                'aria-describedby': 'id_description_help',
                'aria-required': 'true'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': '0,00',
                'step': '0.01',
                'min': '0.01',
                'data-validate': 'true',
                'data-required': 'true',
                'data-positive': 'true',
                'aria-describedby': 'id_amount_help',
                'aria-required': 'true'
            }),
            'transaction_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'aria-describedby': 'id_transaction_date_help',
                'aria-required': 'true'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'aria-describedby': 'id_transaction_type_help',
                'aria-required': 'true'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'aria-describedby': 'id_category_help',
                'aria-required': 'true'
            }),
            'account': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'aria-describedby': 'id_account_help',
                'aria-required': 'true'
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

        # Initialize warnings dictionary to store date-related warnings
        self.warnings = {}

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

        IMPORTANT: Transaction amounts must ALWAYS be positive (greater than 0).
        The transaction type (INCOME/EXPENSE) determines how the amount affects
        the account balance, not the sign of the amount.

        This is different from account balances, which can be negative.
        For transactions, use:
        - Positive amount + transaction_type=INCOME for deposits/income
        - Positive amount + transaction_type=EXPENSE for withdrawals/expenses
        """
        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise forms.ValidationError('O valor é obrigatório')

        if amount <= Decimal('0'):
            raise forms.ValidationError(
                'O valor deve ser maior que zero. '
                'Informe apenas valores positivos. '
                'O tipo da transação (receita ou despesa) determina como o valor afeta o saldo.'
            )

        return amount

    def clean_transaction_date(self):
        """
        Custom validation for transaction_date field.

        Business logic:
        - Allows future dates (for scheduled/planned transactions)
        - Shows a WARNING (not error) for future dates
        - Shows a stronger WARNING for dates more than 1 year in the future
        - Validates that the date is not too far in the past (more than 10 years)

        This supports use cases like:
        - Scheduled bill payments
        - Expected salary deposits
        - Planned expenses
        """
        transaction_date = self.cleaned_data.get('transaction_date')

        if transaction_date is None:
            return transaction_date

        today = date.today()

        # Check if date is too far in the past (more than 10 years)
        ten_years_ago = today - timedelta(days=365 * 10)
        if transaction_date < ten_years_ago:
            raise forms.ValidationError(
                'A data da transação não pode ser anterior a 10 anos atrás. '
                'Verifique se a data está correta.'
            )

        # Check if date is in the future
        if transaction_date > today:
            days_in_future = (transaction_date - today).days

            # Strong warning for dates more than 1 year in the future
            if days_in_future > 365:
                years_ahead = days_in_future / 365
                self.warnings['transaction_date'] = (
                    f'Atenção: Esta data está {years_ahead:.1f} anos no futuro. '
                    'Verifique se a data está correta. '
                    'Transações futuras são úteis para planejamento, mas datas muito distantes podem ser erros de digitação.'
                )
            # Regular warning for future dates (up to 1 year)
            else:
                if days_in_future == 1:
                    days_text = 'amanhã'
                elif days_in_future <= 30:
                    days_text = f'em {days_in_future} dias'
                else:
                    months = days_in_future // 30
                    days_text = f'em aproximadamente {months} meses' if months > 1 else 'em aproximadamente 1 mês'

                self.warnings['transaction_date'] = (
                    f'Nota: Esta transação está agendada para o futuro ({days_text}). '
                    'Ela será contabilizada no saldo, mas ainda não ocorreu.'
                )

        return transaction_date

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


class TransactionFilterForm(forms.Form):
    """
    Form for filtering transactions.
    All fields are optional to allow flexible filtering.
    Querysets for category and account are filtered by user in the view.
    """

    # Transaction type choices matching the Transaction model
    TRANSACTION_TYPE_CHOICES = [
        ('', 'Todos os tipos'),
        (Transaction.INCOME, 'Receita'),
        (Transaction.EXPENSE, 'Despesa'),
    ]

    date_from = forms.DateField(
        required=False,
        label='Data inicial',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
        })
    )

    date_to = forms.DateField(
        required=False,
        label='Data final',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
        })
    )

    transaction_type = forms.ChoiceField(
        required=False,
        label='Tipo de transação',
        choices=TRANSACTION_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
        })
    )

    category = forms.ModelChoiceField(
        required=False,
        label='Categoria',
        queryset=Category.objects.none(),  # Will be set in __init__ based on user
        empty_label='Todas as categorias',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
        })
    )

    account = forms.ModelChoiceField(
        required=False,
        label='Conta',
        queryset=Account.objects.none(),  # Will be set in __init__ based on user
        empty_label='Todas as contas',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
        })
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with user parameter.
        Filters accounts and categories by the logged-in user.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            # Filter accounts: only active accounts belonging to the user
            self.fields['account'].queryset = Account.objects.filter(
                user=self.user,
                is_active=True
            ).order_by('name')

            # Filter categories: all categories belonging to the user
            self.fields['category'].queryset = Category.objects.filter(
                user=self.user
            ).order_by('category_type', 'name')

    def clean(self):
        """
        Custom validation to ensure date_from is not greater than date_to.
        """
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError(
                'A data inicial não pode ser maior que a data final.'
            )

        return cleaned_data
