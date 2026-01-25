from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import CategoryForm
from .models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    """
    Display list of user's transaction categories.
    Separates categories into income and expense types.
    Filters categories to show only those belonging to the current user.
    Includes pagination (20 items per page).
    """
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        """
        Filter categories to only show those belonging to current user.
        Ordered by name (default from model Meta).
        """
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add separate querysets for income and expense categories to context.
        Optimized to use a single database query and split in Python.
        """
        context = super().get_context_data(**kwargs)

        # Get all categories for current user in a single query
        all_categories = list(self.get_queryset())

        # Separate into income and expense categories in Python (no additional DB queries)
        context['income_categories'] = [
            cat for cat in all_categories if cat.category_type == Category.INCOME
        ]
        context['expense_categories'] = [
            cat for cat in all_categories if cat.category_type == Category.EXPENSE
        ]

        return context


class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a new transaction category.
    Automatically associates the category with the current user.
    Sets is_default = False for all user-created categories.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')
    success_message = 'Categoria criada com sucesso!'

    def get_form_kwargs(self):
        """
        Pass the current user to the form for validation.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Set the user field to current user and is_default to False before saving.
        """
        form.instance.user = self.request.user
        form.instance.is_default = False
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update an existing transaction category.
    Verifies that the user owns this category.
    Does NOT allow editing if is_default = True.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')
    success_message = 'Categoria atualizada com sucesso!'

    def get_form_kwargs(self):
        """
        Pass the current user to the form for validation.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        """
        Verify that the current user owns this category.
        """
        category = self.get_object()
        return category.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        """
        Check if category is_default before allowing access to update view.
        Redirect with error message if trying to edit default category.
        """
        category = self.get_object()

        if category.is_default:
            messages.error(
                request,
                'Categorias padrão não podem ser editadas. '
                'Crie uma nova categoria personalizada se desejar.'
            )
            return redirect('categories:list')

        return super().dispatch(request, *args, **kwargs)


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """
    Delete a transaction category.
    Verifies that the user owns this category before allowing deletion.
    Does NOT allow deleting if is_default = True.
    Checks if category has linked transactions (future: when Transaction model exists).
    """
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('categories:list')
    success_message = 'Categoria excluída com sucesso!'

    def test_func(self):
        """
        Verify that the current user owns this category.
        """
        category = self.get_object()
        return category.user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        """
        Check if category is_default before allowing access to delete view.
        Redirect with error message if trying to delete default category.
        """
        category = self.get_object()

        if category.is_default:
            messages.error(
                request,
                'Categorias padrão não podem ser excluídas.'
            )
            return redirect('categories:list')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Override delete to check for linked transactions and add success message.
        SuccessMessageMixin doesn't work with DeleteView by default.
        """
        category = self.get_object()

        # TODO: When Transaction model exists, uncomment this validation
        # Check if category has linked transactions
        # if category.transactions.exists():
        #     messages.error(
        #         request,
        #         'Esta categoria não pode ser excluída pois possui transações vinculadas. '
        #         'Exclua ou mova as transações primeiro.'
        #     )
        #     return redirect('categories:list')

        # For now, just add a placeholder comment since Transaction model doesn't exist yet
        # Future implementation will query: category.transactions.exists()

        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
