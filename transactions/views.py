"""
Transaction views for the Finanpy application.

This module contains views for managing financial transactions including list
with advanced filtering, create, update, delete, and detail views with
automatic balance calculations and query optimization.
"""
from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import TransactionForm, TransactionFilterForm
from .models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    """
    Display list of user's transactions with filtering capabilities.
    Filters transactions to show only those belonging to the current user.
    Supports filtering by date range, transaction type, category, and account.
    Orders by transaction_date descending, then created_at descending.
    Includes pagination (20 items per page).
    Optimizes queries with select_related for account and category.
    Calculates filtered totals for income, expense, and balance.
    """
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        """
        Filter transactions to only show those belonging to current user.
        Apply additional filters based on GET parameters (date_from, date_to,
        transaction_type, category, account).
        Order by transaction_date desc, then created_at desc.
        Use select_related to optimize database queries.
        """
        queryset = Transaction.objects.filter(
            user=self.request.user
        ).select_related(
            'account',
            'category'
        )

        # Apply filters based on GET parameters
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        transaction_type = self.request.GET.get('transaction_type')
        category_id = self.request.GET.get('category')
        account_id = self.request.GET.get('account')

        # Filter by date_from
        if date_from:
            queryset = queryset.filter(transaction_date__gte=date_from)

        # Filter by date_to
        if date_to:
            queryset = queryset.filter(transaction_date__lte=date_to)

        # Filter by transaction_type
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        # Filter by category
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by account
        if account_id:
            queryset = queryset.filter(account_id=account_id)

        return queryset.order_by('-transaction_date', '-created_at')

    def get_context_data(self, **kwargs):
        """
        Add filter form and calculated totals to context.
        Calculate total_income, total_expense, and balance based on filtered queryset.
        """
        context = super().get_context_data(**kwargs)

        # Instantiate filter form with GET data and user
        context['filter_form'] = TransactionFilterForm(
            data=self.request.GET or None,
            user=self.request.user
        )

        # Get the filtered queryset (without pagination)
        filtered_queryset = self.get_queryset()

        # Calculate totals from filtered queryset
        # Use aggregate to sum amounts by transaction type
        income_total = filtered_queryset.filter(
            transaction_type=Transaction.INCOME
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        expense_total = filtered_queryset.filter(
            transaction_type=Transaction.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        # Calculate balance (income - expense)
        balance = income_total - expense_total

        # Add totals to context
        context['total_income'] = income_total
        context['total_expense'] = expense_total
        context['balance'] = balance

        return context


class TransactionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a new transaction.
    Automatically associates the transaction with the current user.
    Sets default transaction_date to today.
    Passes user to form for filtering accounts and categories.
    """
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')
    success_message = 'Transação criada com sucesso!'

    def get_initial(self):
        """
        Set default transaction_date to today.
        """
        initial = super().get_initial()
        initial['transaction_date'] = date.today()
        return initial

    def get_form_kwargs(self):
        """
        Pass the current user to the form for filtering accounts and categories.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Set the user field to current user before saving.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update an existing transaction.
    Verifies that the user owns this transaction.
    Passes user to form for filtering accounts and categories.
    """
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')
    success_message = 'Transação atualizada com sucesso!'

    def get_form_kwargs(self):
        """
        Pass the current user to the form for filtering accounts and categories.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        """
        Verify that the current user owns this transaction.
        """
        transaction = self.get_object()
        return transaction.user == self.request.user


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    Delete a transaction.
    Verifies that the user owns this transaction before allowing deletion.
    Shows confirmation page before deletion.
    """
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:list')
    success_message = 'Transação excluída com sucesso!'

    def test_func(self):
        """
        Verify that the current user owns this transaction.
        """
        transaction = self.get_object()
        return transaction.user == self.request.user

    def delete(self, request, *args, **kwargs):
        """
        Override delete to add success message.
        SuccessMessageMixin doesn't work with DeleteView by default.
        """
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class TransactionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Display detailed information about a transaction.
    Verifies that the user owns this transaction.
    Uses select_related to optimize queries for account and category.
    """
    model = Transaction
    template_name = 'transactions/transaction_detail.html'
    context_object_name = 'transaction'

    def get_queryset(self):
        """
        Use select_related to optimize database queries.
        """
        return Transaction.objects.select_related(
            'account',
            'category'
        )

    def test_func(self):
        """
        Verify that the current user owns this transaction.
        """
        transaction = self.get_object()
        return transaction.user == self.request.user
