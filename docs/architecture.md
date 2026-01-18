# Arquitetura do Projeto

## Visao Geral

O Finanpy segue a arquitetura padrao do Django, organizado em apps modulares com responsabilidades bem definidas.

## Estrutura de Apps

```
finanpy/
├── core/              # Projeto principal Django
│   ├── settings.py    # Configuracoes globais
│   ├── urls.py        # URLs raiz
│   ├── wsgi.py        # WSGI para deploy
│   └── asgi.py        # ASGI para async
│
├── users/             # Autenticacao e usuarios
├── profiles/          # Perfis de usuario
├── accounts/          # Contas bancarias
├── categories/        # Categorias de transacoes
└── transactions/      # Transacoes financeiras
```

## Responsabilidades dos Apps

### core

Configuracoes centrais do projeto Django:
- Settings (banco de dados, apps instalados, middleware)
- URLs raiz
- Configuracoes WSGI/ASGI

### users

Gerenciamento de autenticacao:
- Modelo de usuario customizado (planejado)
- Login/Logout
- Cadastro
- Recuperacao de senha

### profiles

Dados adicionais do usuario:
- Nome, sobrenome
- Telefone
- Avatar

### accounts

Contas bancarias do usuario:
- Conta corrente, poupanca, investimento
- Saldo inicial e atual

### categories

Categorias para classificar transacoes:
- Tipo: receita ou despesa
- Cor para identificacao visual
- Categorias padrao e personalizadas

### transactions

Registro de movimentacoes financeiras:
- Receitas e despesas
- Vinculo com conta e categoria
- Atualizacao automatica de saldo

## Banco de Dados

- **Engine**: SQLite (desenvolvimento)
- **Arquivo**: `db.sqlite3` na raiz do projeto

## Apps Instalados

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'categories',
    'profiles',
    'transactions',
    'users',
]
```

## Modelo de Dados (Planejado)

```
User (1) ──── (1) Profile
  │
  ├──── (*) Account ──── (*) Transaction
  │                            │
  └──── (*) Category ──────────┘
```

### Relacionamentos

- User tem um Profile (OneToOne)
- User possui varias Accounts (ForeignKey)
- User possui varias Categories (ForeignKey)
- Account possui varias Transactions (ForeignKey)
- Category categoriza varias Transactions (ForeignKey)
