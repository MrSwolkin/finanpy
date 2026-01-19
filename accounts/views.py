from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .forms import AccountForm
from .models import Account


class AccountListView(LoginRequiredMixin, ListView):
    """
    Display list of user's bank accounts.
    Filters accounts to show only those belonging to the current user.
    """
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        """
        Filter accounts to only show those belonging to current user.
        Ordered by name (default from model Meta).
        """
        return Account.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add total balance of all accounts to context.
        """
        context = super().get_context_data(**kwargs)
        total = self.get_queryset().aggregate(total=Sum('current_balance'))['total']
        context['total_balance'] = total or 0
        return context


class AccountCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a new bank account.
    Automatically associates the account with the current user.
    Sets current_balance equal to initial_balance via AccountForm.save().
    """
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:list')
    success_message = 'Conta criada com sucesso!'

    def form_valid(self, form):
        """
        Set the user field to current user before saving.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update an existing bank account.
    Only allows editing name and account_type (not initial_balance).
    Verifies that the user owns this account.
    """
    model = Account
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:list')
    success_message = 'Conta atualizada com sucesso!'
    fields = ['name', 'account_type']

    def test_func(self):
        """
        Verify that the current user owns this account.
        """
        account = self.get_object()
        return account.user == self.request.user

    def get_form(self, form_class=None):
        """
        Override get_form to apply TailwindCSS styling to widgets.
        """
        form = super().get_form(form_class)

        # Apply TailwindCSS classes to widgets
        form.fields['name'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition duration-200',
            'placeholder': 'Ex: Banco do Brasil - Conta Corrente',
        })
        form.fields['account_type'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition duration-200',
        })

        # Set Portuguese labels
        form.fields['name'].label = 'Nome da Conta'
        form.fields['account_type'].label = 'Tipo de Conta'

        # Set help texts
        form.fields['name'].help_text = 'Digite um nome descritivo para identificar sua conta'
        form.fields['account_type'].help_text = 'Selecione o tipo de conta bancária'

        return form


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    Delete a bank account.
    Verifies that the user owns this account before allowing deletion.
    """
    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('accounts:list')
    success_message = 'Conta excluída com sucesso!'

    def test_func(self):
        """
        Verify that the current user owns this account.
        """
        account = self.get_object()
        return account.user == self.request.user

    def delete(self, request, *args, **kwargs):
        """
        Override delete to add success message.
        SuccessMessageMixin doesn't work with DeleteView by default.
        """
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class AccountDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Display detailed information about a bank account.
    Verifies that the user owns this account.
    Future: Will include list of transactions for this account.
    """
    model = Account
    template_name = 'accounts/account_detail.html'
    context_object_name = 'account'

    def test_func(self):
        """
        Verify that the current user owns this account.
        """
        account = self.get_object()
        return account.user == self.request.user
