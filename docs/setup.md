# Setup do Projeto

## Requisitos

- Python 3.13+
- pip

## Instalacao

### 1. Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd finanpy
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar ambiente virtual

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Aplicar migracoes

```bash
python manage.py migrate
```

### 6. Criar superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Rodar servidor de desenvolvimento

```bash
python manage.py runserver
```

O projeto estara disponivel em `http://127.0.0.1:8000/`

## Dependencias Atuais

| Pacote | Versao |
|--------|--------|
| Django | 6.0.1 |
| asgiref | 3.11.0 |
| sqlparse | 0.5.5 |

## Comandos Uteis

| Comando | Descricao |
|---------|-----------|
| `python manage.py runserver` | Inicia servidor de desenvolvimento |
| `python manage.py migrate` | Aplica migracoes pendentes |
| `python manage.py makemigrations` | Cria novas migracoes |
| `python manage.py createsuperuser` | Cria usuario admin |
| `python manage.py shell` | Abre shell interativo do Django |

## Estrutura de Diretorios

```
finanpy/
├── core/           # Configuracoes do projeto Django
├── users/          # App de usuarios
├── profiles/       # App de perfis
├── accounts/       # App de contas bancarias
├── categories/     # App de categorias
├── transactions/   # App de transacoes
├── venv/           # Ambiente virtual (ignorado pelo git)
├── manage.py       # Script de gerenciamento Django
├── requirements.txt
└── PRD.md          # Documento de requisitos do produto
```
