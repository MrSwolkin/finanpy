# Arquitetura do Projeto Finanpy

## Visão Geral

O Finanpy segue a arquitetura padrão do Django (MTV - Model-Template-View), organizado em apps modulares com responsabilidades bem definidas. O projeto utiliza Class-Based Views (CBVs) com mixins para autenticação e autorização.

## Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|------------|--------|
| Backend | Django | 6.0+ |
| Linguagem | Python | 3.13+ |
| Banco de Dados | SQLite | - |
| Frontend | TailwindCSS | 4.0 |
| Templates | Django Template Language | - |
| Integração CSS | django-tailwind | 4.0+ |

## Estrutura de Diretórios

```
finanpy/
├── core/                   # Projeto principal Django
│   ├── __init__.py
│   ├── settings.py         # Configurações globais
│   ├── urls.py             # URLs raiz
│   ├── views.py            # DashboardView
│   ├── wsgi.py             # Servidor WSGI
│   ├── asgi.py             # Servidor ASGI
│   └── templatetags/       # Filtros customizados
│       ├── __init__.py
│       └── currency_filters.py
│
├── users/                  # Autenticação
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py            # Registro no admin
│   ├── apps.py
│   ├── forms.py            # CustomUserCreationForm
│   ├── models.py           # CustomUser, CustomUserManager
│   ├── tests.py
│   ├── urls.py
│   └── views.py            # SignUpView, CustomLoginView, etc.
│
├── profiles/               # Perfis de usuário
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # ProfileForm
│   ├── models.py           # Profile
│   ├── signals.py          # Criação automática de perfil
│   ├── tests.py
│   ├── urls.py
│   └── views.py            # ProfileDetailView, ProfileUpdateView
│
├── accounts/               # Contas bancárias
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # AccountForm
│   ├── models.py           # Account
│   ├── tests.py
│   ├── urls.py
│   └── views.py            # AccountListView, AccountCreateView, etc.
│
├── categories/             # Categorias de transações
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── create_default_categories.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # CategoryForm
│   ├── models.py           # Category
│   ├── tests.py
│   ├── urls.py
│   └── views.py            # CategoryListView, CategoryCreateView, etc.
│
├── transactions/           # Transações financeiras
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # TransactionForm, TransactionFilterForm
│   ├── models.py           # Transaction
│   ├── signals.py          # Atualização automática de saldo
│   ├── tests.py
│   ├── urls.py
│   └── views.py            # TransactionListView, etc.
│
├── theme/                  # TailwindCSS
│   ├── static/             # CSS compilado
│   └── static_src/         # Arquivos fonte
│       ├── src/
│       │   └── styles.css
│       ├── package.json
│       └── tailwind.config.js
│
├── templates/              # Templates globais
│   ├── base.html           # Template base
│   ├── partials/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   └── messages.html
│   ├── components/
│   │   ├── button.html
│   │   ├── card.html
│   │   └── form_field.html
│   ├── users/              # Templates de autenticação
│   ├── profiles/           # Templates de perfil
│   ├── accounts/           # Templates de contas
│   ├── categories/         # Templates de categorias
│   ├── transactions/       # Templates de transações
│   ├── dashboard/          # Templates do dashboard
│   └── landing/            # Landing page
│
├── static/                 # Arquivos estáticos
│   ├── js/
│   │   ├── navbar.js
│   │   └── transactions.js
│   └── images/
│
├── media/                  # Uploads de usuários
│   └── avatars/
│
├── docs/                   # Documentação
│
├── .env                    # Variáveis de ambiente
├── .gitignore
├── manage.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── CLAUDE.md
└── TASKS.md
```

## Apps e Responsabilidades

### core

Configurações centrais do projeto Django:

| Arquivo | Responsabilidade |
|---------|------------------|
| `settings.py` | Configurações globais (DB, apps, middleware, etc.) |
| `urls.py` | Roteamento raiz, inclusão de URLs dos apps |
| `views.py` | DashboardView com analytics e filtros de período |
| `templatetags/` | Filtros customizados (moeda, datas) |

**DashboardView Features:**
- Cálculo de saldo total de todas as contas ativas
- Filtro por período (mês atual, anterior, 3 meses, ano, customizado)
- Agregação de receitas e despesas
- Top 5 categorias de despesa
- Últimas 5 transações

### users

Gerenciamento de autenticação com email:

| Componente | Descrição |
|------------|-----------|
| `CustomUser` | Modelo de usuário com email como identificador |
| `CustomUserManager` | Manager para criação de usuários |
| `SignUpView` | Cadastro com login automático |
| `CustomLoginView` | Login com mensagem de boas-vindas |
| `CustomLogoutView` | Logout com mensagem de despedida |
| Password Reset Views | Fluxo completo de recuperação de senha |

**Características:**
- Autenticação baseada em email (sem username)
- Validação de senha forte
- Prevenção contra enumeração de emails
- Proteção contra open redirect

### profiles

Dados adicionais do usuário:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `user` | OneToOneField | Relacionamento com CustomUser |
| `first_name` | CharField | Nome |
| `last_name` | CharField | Sobrenome |
| `phone` | CharField | Telefone (opcional) |
| `avatar` | ImageField | Foto de perfil (opcional) |
| `created_at` | DateTimeField | Data de criação |
| `updated_at` | DateTimeField | Data de atualização |

**Signals:**
- `post_save` em User cria Profile automaticamente

### accounts

Gerenciamento de contas bancárias:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `user` | ForeignKey | Proprietário da conta |
| `name` | CharField | Nome da conta |
| `account_type` | CharField | Tipo (checking, savings, investment, other) |
| `initial_balance` | DecimalField | Saldo inicial |
| `current_balance` | DecimalField | Saldo atual |
| `is_active` | BooleanField | Status ativo/inativo |

**Tipos de Conta:**
- `checking` - Conta Corrente
- `savings` - Poupança
- `investment` - Investimento
- `other` - Outro

**Validações:**
- Saldo negativo permitido (cheque especial)
- Aviso de transações vinculadas ao excluir

### categories

Categorização de transações:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `user` | ForeignKey | Proprietário |
| `name` | CharField | Nome da categoria |
| `category_type` | CharField | Tipo (income, expense) |
| `color` | CharField | Cor em formato hex |
| `is_default` | BooleanField | Categoria padrão |

**Categorias Padrão (Receita):**
- Salário (#10b981)
- Freelance (#3b82f6)
- Investimentos (#8b5cf6)
- Outros (#6b7280)

**Categorias Padrão (Despesa):**
- Alimentação (#ef4444)
- Transporte (#f59e0b)
- Moradia (#06b6d4)
- Saúde (#ec4899)
- Lazer (#14b8a6)
- Educação (#6366f1)
- Outros (#6b7280)

**Proteções:**
- Categorias padrão não podem ser editadas/excluídas
- Categorias com transações não podem ser excluídas

### transactions

Registro de movimentações financeiras:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `user` | ForeignKey | Proprietário |
| `account` | ForeignKey | Conta vinculada |
| `category` | ForeignKey | Categoria |
| `description` | CharField | Descrição |
| `amount` | DecimalField | Valor (sempre positivo) |
| `transaction_date` | DateField | Data da transação |
| `transaction_type` | CharField | Tipo (income, expense) |

**Validações:**
- Valor deve ser positivo (> 0)
- Categoria deve corresponder ao tipo
- Datas futuras permitidas com aviso
- Datas > 10 anos no passado bloqueadas

**Signals:**
- `pre_save` - Reverte saldo antigo antes de atualizar
- `post_save` - Aplica novo valor ao saldo
- `post_delete` - Estorna valor ao excluir

## Modelo de Dados

### Diagrama de Relacionamentos

```
┌──────────────┐
│  CustomUser  │
└──────┬───────┘
       │
       │ OneToOne
       ▼
┌──────────────┐
│   Profile    │
└──────────────┘
       │
       │ ForeignKey (1:N)
       ├───────────────────┐
       ▼                   ▼
┌──────────────┐    ┌──────────────┐
│   Account    │    │   Category   │
└──────┬───────┘    └──────┬───────┘
       │                   │
       │   ForeignKey      │ ForeignKey
       └───────┬───────────┘
               ▼
       ┌──────────────┐
       │ Transaction  │
       └──────────────┘
```

### Relacionamentos

| De | Para | Tipo | Descrição |
|----|------|------|-----------|
| User | Profile | OneToOne | Cada usuário tem um perfil |
| User | Account | ForeignKey | Usuário possui várias contas |
| User | Category | ForeignKey | Usuário possui várias categorias |
| User | Transaction | ForeignKey | Usuário possui várias transações |
| Account | Transaction | ForeignKey | Conta possui várias transações |
| Category | Transaction | ForeignKey | Categoria possui várias transações |

### Índices de Banco de Dados

| Modelo | Campos Indexados |
|--------|------------------|
| Account | `user`, `account_type` |
| Category | `user`, `category_type` |
| Transaction | `user`, `transaction_type`, `transaction_date` |

## Padrões de Desenvolvimento

### Views

Todas as views utilizam Class-Based Views com mixins:

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

class MyListView(LoginRequiredMixin, ListView):
    model = MyModel

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
```

### Formulários

Formulários utilizam widgets customizados com TailwindCSS:

```python
class MyForm(forms.ModelForm):
    class Meta:
        widgets = {
            'field': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-700 ...',
            })
        }
```

### Queries

Otimização de queries com select_related:

```python
def get_queryset(self):
    return Transaction.objects.filter(
        user=self.request.user
    ).select_related('account', 'category')
```

### Signals

Automatização via signals:

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

## Fluxo de Dados

### Criação de Transação

```
1. Usuário submete formulário
   ↓
2. TransactionCreateView.form_valid()
   ↓
3. Transaction.save() dispara signal pre_save
   ↓
4. Signal post_save atualiza Account.current_balance
   ↓
5. Redirect para lista de transações
```

### Autenticação

```
1. Usuário submete credenciais
   ↓
2. CustomLoginView autentica
   ↓
3. Sessão criada
   ↓
4. Redirect para dashboard
```

## Configurações Importantes

### settings.py

```python
# Modelo de usuário customizado
AUTH_USER_MODEL = 'users.CustomUser'

# Autenticação
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'landing'

# Idioma e timezone
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

# TailwindCSS
TAILWIND_APP_NAME = 'theme'
```

## Segurança

### Isolamento de Dados

Todas as queries são filtradas por usuário:

```python
queryset = Model.objects.filter(user=request.user)
```

### Proteções Implementadas

- CSRF protection ativo
- LoginRequiredMixin em todas as views protegidas
- UserPassesTestMixin para verificação de propriedade
- Validação de redirect para prevenir open redirect
- Prevenção de enumeração de email

---

*Última atualização: Janeiro 2026*
