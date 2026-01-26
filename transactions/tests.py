from datetime import date, timedelta
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from transactions.forms import TransactionForm
from transactions.models import Transaction
from accounts.models import Account
from categories.models import Category


User = get_user_model()


class TransactionFormDateValidationTestCase(TestCase):
    """
    Tests for TransactionForm date validation.
    Validates future dates warnings and past dates errors.
    """

    def setUp(self):
        """Create test user, account, and category."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        self.account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type=Account.CHECKING,
            initial_balance=Decimal('1000.00'),
            current_balance=Decimal('1000.00'),
            is_active=True
        )

        self.category = Category.objects.create(
            user=self.user,
            name='Test Expense',
            category_type=Transaction.EXPENSE,
            color='#FF0000'
        )

        self.today = date.today()

    def _get_form_data(self, transaction_date=None):
        """Helper to create valid form data."""
        return {
            'description': 'Test Transaction',
            'amount': Decimal('100.00'),
            'transaction_date': transaction_date or self.today,
            'transaction_type': Transaction.EXPENSE,
            'category': self.category.pk,
            'account': self.account.pk,
        }

    def test_today_date_no_warning(self):
        """Test that today's date doesn't generate a warning."""
        form = TransactionForm(data=self._get_form_data(), user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.warnings, {})

    def test_past_date_no_warning(self):
        """Test that past dates (within 10 years) don't generate warnings."""
        past_date = self.today - timedelta(days=365)
        data = self._get_form_data(transaction_date=past_date)
        form = TransactionForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.warnings, {})

    def test_tomorrow_warning(self):
        """Test that tomorrow generates a friendly warning."""
        tomorrow = self.today + timedelta(days=1)
        data = self._get_form_data(transaction_date=tomorrow)
        form = TransactionForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertIn('transaction_date', form.warnings)
        self.assertIn('amanhã', form.warnings['transaction_date'])

    def test_future_days_warning(self):
        """Test that future dates (7 days) generate warning with day count."""
        future_date = self.today + timedelta(days=7)
        data = self._get_form_data(transaction_date=future_date)
        form = TransactionForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertIn('transaction_date', form.warnings)
        self.assertIn('em 7 dias', form.warnings['transaction_date'])

    def test_future_months_warning(self):
        """Test that future dates (3 months) generate warning with month count."""
        future_date = self.today + timedelta(days=90)
        data = self._get_form_data(transaction_date=future_date)
        form = TransactionForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertIn('transaction_date', form.warnings)
        self.assertIn('aproximadamente 3 meses', form.warnings['transaction_date'])

    def test_future_one_year_regular_warning(self):
        """Test that exactly 1 year in future gets regular warning."""
        future_date = self.today + timedelta(days=365)
        data = self._get_form_data(transaction_date=future_date)
        form = TransactionForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertIn('transaction_date', form.warnings)
        # Should be regular warning (not strong warning)
        self.assertIn('Nota:', form.warnings['transaction_date'])
        self.assertNotIn('Atenção:', form.warnings['transaction_date'])

    def test_future_two_years_strong_warning(self):
        """Test that 2 years in future generates strong warning."""
        future_date = self.today + timedelta(days=730)
        data = self._get_form_data(transaction_date=future_date)
        form = TransactionForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertIn('transaction_date', form.warnings)
        self.assertIn('Atenção:', form.warnings['transaction_date'])
        self.assertIn('2.0 anos no futuro', form.warnings['transaction_date'])

    def test_ten_years_past_no_error(self):
        """Test that exactly 10 years ago is still valid (edge case)."""
        ten_years_ago = self.today - timedelta(days=365 * 10)
        data = self._get_form_data(transaction_date=ten_years_ago)
        form = TransactionForm(data=data, user=self.user)
        # Should be valid (>= 10 years ago is the limit)
        self.assertTrue(form.is_valid())

    def test_eleven_years_past_error(self):
        """Test that more than 10 years ago raises validation error."""
        eleven_years_ago = self.today - timedelta(days=365 * 11)
        data = self._get_form_data(transaction_date=eleven_years_ago)
        form = TransactionForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('transaction_date', form.errors)
        self.assertIn('10 anos atrás', form.errors['transaction_date'][0])

    def test_warning_does_not_prevent_save(self):
        """Test that warnings don't prevent form from being valid and saved."""
        future_date = self.today + timedelta(days=30)
        data = self._get_form_data(transaction_date=future_date)
        form = TransactionForm(data=data, user=self.user)

        # Form should be valid despite warning
        self.assertTrue(form.is_valid())
        self.assertIn('transaction_date', form.warnings)

        # Should be able to save
        transaction = form.save(commit=False)
        transaction.user = self.user
        transaction.save()

        # Verify transaction was saved
        self.assertEqual(Transaction.objects.count(), 1)
        saved_transaction = Transaction.objects.first()
        self.assertEqual(saved_transaction.transaction_date, future_date)
