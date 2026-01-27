# Setup do Projeto Finanpy

Guia completo para instalação e configuração do ambiente de desenvolvimento.

## Requisitos do Sistema

### Obrigatórios
- **Python** 3.10 ou superior (recomendado: 3.13+)
- **pip** (gerenciador de pacotes Python)
- **Git** (controle de versão)

### Automáticos
- **Node.js** - Instalado automaticamente pelo django-tailwind

## Instalação Passo a Passo

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd finanpy
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv
```

### 3. Ativar Ambiente Virtual

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

> **Nota:** O prompt do terminal deve mudar para indicar `(venv)` no início.

### 4. Instalar Dependências Python

```bash
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
touch .env  # macOS/Linux
# ou crie manualmente no Windows
```

Adicione o seguinte conteúdo:

```env
# Configurações de Segurança
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Configurações de Email (opcional para desenvolvimento)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

#### Gerando uma SECRET_KEY Segura

Execute o comando abaixo para gerar uma chave segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie a saída e cole no arquivo `.env`.

### 6. Instalar TailwindCSS

```bash
python manage.py tailwind install
```

Este comando instala as dependências do Node.js necessárias para o TailwindCSS.

### 7. Aplicar Migrações do Banco de Dados

```bash
python manage.py migrate
```

### 8. Criar Superusuário (Opcional)

Para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

Siga as instruções para definir email e senha.

### 9. Verificar Instalação

Execute o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` no navegador.

## Desenvolvimento

### Executando a Aplicação

Para desenvolvimento, você precisa de **dois terminais**:

**Terminal 1 - Servidor Django:**
```bash
python manage.py runserver
```

**Terminal 2 - TailwindCSS (hot reload):**
```bash
python manage.py tailwind start
```

### Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `python manage.py runserver` | Inicia servidor de desenvolvimento |
| `python manage.py tailwind start` | Inicia Tailwind com hot reload |
| `python manage.py tailwind build` | Compila CSS para produção |
| `python manage.py migrate` | Aplica migrações pendentes |
| `python manage.py makemigrations` | Cria novas migrações |
| `python manage.py createsuperuser` | Cria usuário admin |
| `python manage.py shell` | Abre shell interativo do Django |
| `python manage.py test` | Executa testes automatizados |
| `python manage.py collectstatic` | Coleta arquivos estáticos |

## Dependências Principais

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| Django | 6.0+ | Framework web |
| django-tailwind | 4.0+ | Integração TailwindCSS |
| django-browser-reload | - | Hot reload do navegador |
| python-decouple | - | Gerenciamento de variáveis de ambiente |
| Pillow | - | Processamento de imagens (avatares) |

## Estrutura de Diretórios

```
finanpy/
├── core/               # Configurações do projeto Django
│   ├── settings.py     # Configurações principais
│   ├── urls.py         # URLs raiz
│   ├── views.py        # DashboardView
│   └── templatetags/   # Filtros customizados
│
├── users/              # Autenticação de usuários
│   ├── models.py       # CustomUser (email-based)
│   ├── views.py        # Login, Signup, Password Reset
│   └── forms.py        # Formulários de autenticação
│
├── profiles/           # Perfis de usuário
│   ├── models.py       # Profile (nome, telefone, avatar)
│   ├── views.py        # Visualização e edição de perfil
│   └── signals.py      # Criação automática de perfil
│
├── accounts/           # Contas bancárias
│   ├── models.py       # Account (tipos, saldos)
│   └── views.py        # CRUD de contas
│
├── categories/         # Categorias de transações
│   ├── models.py       # Category (tipo, cor)
│   └── management/     # Comando de categorias padrão
│
├── transactions/       # Transações financeiras
│   ├── models.py       # Transaction
│   ├── views.py        # CRUD com filtros
│   └── signals.py      # Atualização de saldos
│
├── theme/              # Configuração TailwindCSS
│   └── static_src/     # Arquivos fonte do Tailwind
│
├── templates/          # Templates globais
│   ├── base.html       # Template base
│   └── partials/       # Componentes reutilizáveis
│
├── static/             # Arquivos estáticos
│   └── js/             # JavaScript
│
├── media/              # Uploads de usuários
│   └── avatars/        # Fotos de perfil
│
├── docs/               # Documentação
│
├── .env                # Variáveis de ambiente (não commitado)
├── .env.example        # Exemplo de variáveis
├── requirements.txt    # Dependências Python
├── manage.py           # Script de gerenciamento
└── db.sqlite3          # Banco de dados (dev)
```

## Solução de Problemas

### Erro: "No module named 'decouple'"

```bash
pip install python-decouple
```

### Erro: "SECRET_KEY not found"

Verifique se o arquivo `.env` existe e contém a variável `SECRET_KEY`.

### Erro: "TailwindCSS not building"

```bash
python manage.py tailwind install
python manage.py tailwind build
```

### Erro: "Permission denied" ao ativar venv

**Windows (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "Port already in use"

```bash
python manage.py runserver 8001  # Use outra porta
```

## Configuração para Produção

Consulte o arquivo `docs/deployment.md` para instruções de deploy.

---

*Última atualização: Janeiro 2026*
