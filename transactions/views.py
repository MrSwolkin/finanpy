from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import TransactionForm
from .models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    """
    Display list of user's transactions.
    Filters transactions to show only those belonging to the current user.
    Orders by transaction_date descending, then created_at descending.
    Includes pagination (20 items per page).
    Optimizes queries with select_related for account and category.
    """
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        """
        Filter transactions to only show those belonging to current user.
        Order by transaction_date desc, then created_at desc.
        Use select_related to optimize database queries.
        """
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related(
            'account',
            'category'
        ).order_by('-transaction_date', '-created_at')


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
