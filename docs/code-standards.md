# Padroes de Codigo

## Convencoes Gerais

### Linguagem

- **Codigo**: Ingles (nomes de variaveis, funcoes, classes, comentarios tecnicos)
- **Interface**: Portugues brasileiro (textos exibidos ao usuario, labels, mensagens)

### Estilo

- Seguir PEP8
- Usar aspas simples para strings (`'texto'`)
- Indentacao com 4 espacos

## Python/Django

### Nomenclatura

| Tipo | Convencao | Exemplo |
|------|-----------|---------|
| Classes | PascalCase | `UserProfile`, `BankAccount` |
| Funcoes | snake_case | `get_user_balance()`, `create_transaction()` |
| Variaveis | snake_case | `current_balance`, `user_id` |
| Constantes | UPPER_SNAKE_CASE | `MAX_TRANSACTIONS`, `DEFAULT_CURRENCY` |
| Apps Django | snake_case (singular) | `user`, `account`, `transaction` |

### Models

```python
from django.db import models

class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Receita'),
        (EXPENSE, 'Despesa'),
    ]

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transacao'
        verbose_name_plural = 'Transacoes'

    def __str__(self):
        return f'{self.description} - {self.amount}'
```

### Views

- Preferir Class-Based Views (CBV)
- Usar mixins para reutilizacao (`LoginRequiredMixin`, etc)

```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
```

### Forms

```python
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'transaction_type', 'category', 'account']
        labels = {
            'description': 'Descricao',
            'amount': 'Valor',
            'transaction_type': 'Tipo',
            'category': 'Categoria',
            'account': 'Conta',
        }
```

### URLs

```python
from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='list'),
    path('create/', views.TransactionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TransactionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete'),
]
```

## Organizacao de Arquivos

Cada app deve seguir a estrutura:

```
app_name/
├── migrations/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py        # Formularios
├── models.py       # Modelos
├── signals.py      # Signals (quando necessario)
├── tests.py        # Testes
├── urls.py         # URLs do app
└── views.py        # Views
```

## Boas Praticas

### Seguranca

- Nunca commitar `SECRET_KEY` real
- Usar variaveis de ambiente para configuracoes sensiveis
- Validar dados no backend
- Proteger contra CSRF (ja habilitado no Django)
- Filtrar querysets por usuario logado

### Performance

- Usar `select_related()` para ForeignKey
- Usar `prefetch_related()` para relacoes reversas
- Implementar paginacao em listagens
- Criar indices para campos frequentemente consultados

### Commits

Mensagens de commit em ingles, descritivas:

```
feat: add transaction list view with filters
fix: correct balance calculation on transaction delete
refactor: extract common form validation to mixin
```
