## Lista de Tarefas

### Sprint 0 - Configuração Inicial (Semana 1)

#### Tarefa 1: Setup do Projeto Django
- [X] 1.1 - Criar ambiente virtual Python
  - Instalar Python 3.10+
  - Criar venv: `python -m venv venv`
  - Ativar venv
- [X] 1.2 - Instalar Django e dependências
  - Django 5+
  - django-tailwind e django-tailwind[reload]
  - Pillow (para avatares)
  - python-decouple (variáveis de ambiente)
- [X] 1.3 - Criar projeto Django
  - `django-admin startproject core .`
  - Verificar estrutura criada
  - Testar servidor: `python manage.py runserver`
- [X] 1.4 - Configurar settings.py inicial
  - Definir SECRET_KEY
  - Configurar ALLOWED_HOSTS
  - Definir TIME_ZONE = 'America/Sao_Paulo'
  - Configurar LANGUAGE_CODE = 'pt-br'
  - Configurar STATIC_URL e STATIC_ROOT
  - Configurar MEDIA_URL e MEDIA_ROOT

#### Tarefa 2: Criar Apps Django
- [X] 2.1 - Criar app users
  - `python manage.py startapp users`
  - Adicionar em INSTALLED_APPS
- [X] 2.2 - Criar app profiles
  - `python manage.py startapp profiles`
  - Adicionar em INSTALLED_APPS
- [X] 2.3 - Criar app accounts
  - `python manage.py startapp accounts`
  - Adicionar em INSTALLED_APPS
- [X] 2.4 - Criar app categories
  - `python manage.py startapp categories`
  - Adicionar em INSTALLED_APPS
- [X] 2.5 - Criar app transactions
  - `python manage.py startapp transactions`
  - Adicionar em INSTALLED_APPS

#### Tarefa 3: Configurar TailwindCSS com django-tailwind
- [X] 3.1 - Instalar django-tailwind
  - `pip install django-tailwind`
  - `pip install 'django-tailwind[reload]'` (para hot reload)
- [X] 3.2 - Adicionar ao INSTALLED_APPS
  - 'tailwind' em settings.py
  - Antes dos apps do projeto
- [X] 3.3 - Criar app theme
  - `python manage.py tailwind init`
  - Nome sugerido: 'theme'
  - Adicionar 'theme' ao INSTALLED_APPS
- [X] 3.4 - Configurar TAILWIND_APP_NAME
  - settings.py: TAILWIND_APP_NAME = 'theme'
- [X] 3.5 - Configurar INTERNAL_IPS (para reload)
  - settings.py: INTERNAL_IPS = ['127.0.0.1']
- [X] 3.6 - Instalar dependências do Tailwind
  - `python manage.py tailwind install`
  - Instala Node.js automaticamente via django-tailwind
- [X] 3.7 - Customizar theme/static_src/tailwind.config.js
  - Configurar tema customizado (cores escuras)
  - Adicionar gradientes personalizados
  - Configurar content paths (já vem pré-configurado)
- [X] 3.8 - Testar build
  - `python manage.py tailwind build`
  - Verificar CSS gerado
- [X] 3.9 - Criar estrutura de diretórios static adicional
  - static/js/
  - static/images/

#### Tarefa 4: Configurar Templates Base
- [X] 4.1 - Criar diretório templates
  - templates/
  - templates/base/
  - templates/partials/
- [X] 4.2 - Criar base.html
  - Estrutura HTML5
  - {% load static tailwind_tags %} no topo
  - {% tailwind_css %} no head para incluir CSS
  - Definir blocks: title, content, extra_css, extra_js
  - Adicionar meta tags responsivas
- [X] 4.3 - Configurar TEMPLATES em settings.py
  - Definir DIRS com caminho de templates
  - Configurar context_processors
- [X] 4.4 - Criar template para mensagens
  - templates/partials/messages.html
  - Usar Django messages framework
  - Estilizar com TailwindCSS (success, error, warning, info)

#### Tarefa 5: Git e Controle de Versão
- [X] 5.1 - Inicializar repositório Git
  - `git init`
- [X] 5.2 - Revise e se necessário adicine ao .gitignore
  - Adicionar venv/
  - Adicionar __pycache__/
  - Adicionar *.pyc
  - Adicionar db.sqlite3
  - Adicionar .env
  - Adicionar theme/static_src/node_modules/ (gerado por django-tailwind)
  - Adicionar theme/static/ (CSS compilado)
- [X] 5.3 - Criar README.md
  - Descrição do projeto
  - Instruções de setup
  - Comandos principais
  - Comando para rodar Tailwind: `python manage.py tailwind start`
- [X] 5.4 - Primeiro commit
  - `git add .`
  - `git commit -m "Initial project setup"`

**Nota sobre desenvolvimento:**
Durante o desenvolvimento, usar `python manage.py tailwind start` em um terminal separado para hot reload automático do CSS ao editar templates.

---

### Sprint 1 - Autenticação e Usuários (Semana 2)

#### Tarefa 6: Modelo de Usuário Customizado
- [X] 6.1 - Criar CustomUser model em users/models.py
  - Herdar de AbstractUser
  - Definir USERNAME_FIELD = 'email'
  - Definir REQUIRED_FIELDS = []
  - Adicionar campo email único
  - Remover campo username
- [X] 6.2 - Criar CustomUserManager
  - Implementar create_user()
  - Implementar create_superuser()
  - Validar email obrigatório
- [X] 6.3 - Configurar AUTH_USER_MODEL em settings.py
  - AUTH_USER_MODEL = 'users.CustomUser'
- [X] 6.4 - Criar e aplicar migrations
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- [X] 6.5 - Registrar model no admin
  - users/admin.py
  - Usar UserAdmin customizado
  - Configurar list_display, search_fields

#### Tarefa 7: Modelo de Profile
- [X] 7.1 - Criar Profile model em profiles/models.py
  - Campo user (OneToOneField com User)
  - Campo first_name (CharField)
  - Campo last_name (CharField)
  - Campo phone (CharField, opcional)
  - Campo avatar (ImageField, opcional)
  - Campo created_at (DateTimeField)
  - Campo updated_at (DateTimeField)
  - Método __str__
- [X] 7.2 - Criar signal para criação automática de Profile
  - profiles/signals.py
  - Signal post_save do User
  - Criar Profile ao criar User
- [X] 7.3 - Configurar signal em apps.py
  - profiles/apps.py
  - Importar signals no ready()
- [X] 7.4 - Criar e aplicar migrations
  - `python manage.py makemigrations profiles`
  - `python manage.py migrate profiles`
- [X] 7.5 - Registrar Profile no admin
  - profiles/admin.py
  - Configurar list_display

#### Tarefa 8: Views de Autenticação
- [X] 8.1 - Criar view de cadastro (SignUpView)
  - users/views.py
  - Class-based view (CreateView)
  - Form com email, password1, password2
  - Validações de senha
  - Login automático após cadastro
  - Redirect para dashboard
- [X] 8.2 - Criar UserCreationForm customizado
  - users/forms.py
  - Basear em UserCreationForm do Django
  - Campos: email, password1, password2
  - Validações customizadas
  - Help texts em português
- [X] 8.3 - Criar view de login (LoginView)
  - users/views.py
  - Usar LoginView do Django
  - Customizar template
  - Configurar success_url
- [X] 8.4 - Criar view de logout (LogoutView)
  - users/views.py
  - Usar LogoutView do Django
  - Redirect para home
- [X] 8.5 - Configurar URLs de autenticação
  - users/urls.py criar arquivo
  - Adicionar rotas: signup/, login/, logout/
  - Incluir em core/urls.py

#### Tarefa 9: Templates de Autenticação
- [X] 9.1 - Criar estrutura de templates users
  - templates/users/
- [X] 9.2 - Criar template de cadastro
  - templates/users/signup.html
  - Herdar de base.html
  - Formulário estilizado com TailwindCSS
  - Link para login
  - Validações visuais
- [X] 9.3 - Criar template de login
  - templates/users/login.html
  - Formulário com email e senha
  - Checkbox "Lembrar-me"
  - Link para cadastro
  - Link para recuperação de senha
- [X] 9.4 - Estilizar forms com TailwindCSS
  - Inputs com bg-gray-700
  - Borders e focus states
  - Labels em text-gray-300
  - Botões com gradiente
  - Mensagens de erro em red

#### Tarefa 10: Recuperação de Senha
- [X] 10.1 - Configurar backend de email
  - settings.py
  - EMAIL_BACKEND para console (dev)
  - Preparar para SMTP (prod futuro)
- [X] 10.2 - Criar views de recuperação
  - Usar PasswordResetView
  - PasswordResetDoneView
  - PasswordResetConfirmView
  - PasswordResetCompleteView
- [X] 10.3 - Criar templates de recuperação
  - password_reset_form.html
  - password_reset_done.html
  - password_reset_confirm.html
  - password_reset_complete.html
- [X] 10.4 - Configurar URLs de recuperação
  - password-reset/
  - password-reset/done/
  - password-reset-confirm/<uidb64>/<token>/
  - password-reset-complete/
- [X] 10.5 - Estilizar templates com TailwindCSS
  - Manter consistência visual
  - Cards e formulários
  - Mensagens informativas

---

### Sprint 2 - Perfil de Usuário (Semana 3)

#### Tarefa 11: Views de Perfil
- [X] 11.1 - Criar ProfileDetailView
  - profiles/views.py
  - Class-based view (DetailView)
  - Obter perfil do usuário logado
  - LoginRequiredMixin
- [X] 11.2 - Criar ProfileUpdateView
  - profiles/views.py
  - Class-based view (UpdateView)
  - Form com first_name, last_name, phone, avatar
  - Validações
  - Success message
- [X] 11.3 - Criar ProfileForm
  - profiles/forms.py
  - ModelForm do Profile
  - Campos editáveis
  - Widgets customizados
  - Labels em português
- [X] 11.4 - Configurar URLs de perfil
  - profiles/urls.py criar arquivo
  - profile/ (detail)
  - profile/edit/ (update)
  - Incluir em core/urls.py

#### Tarefa 12: Templates de Perfil
- [X] 12.1 - Criar estrutura templates profiles
  - templates/profiles/
- [X] 12.2 - Criar template de visualização
  - templates/profiles/profile_detail.html
  - Exibir avatar (ou placeholder)
  - Exibir todas informações
  - Botão "Editar Perfil"
  - Cards estilizados
- [X] 12.3 - Criar template de edição
  - templates/profiles/profile_form.html
  - Formulário completo
  - Preview de avatar
  - Botões Salvar e Cancelar
- [X] 12.4 - Adicionar link no menu
  - Navbar com link "Perfil"
  - Acessível de todas as páginas

#### Tarefa 13: Upload de Avatar
- [X] 13.1 - Configurar MEDIA settings
  - settings.py
  - MEDIA_URL = '/media/'
  - MEDIA_ROOT = BASE_DIR / 'media'
- [X] 13.2 - Configurar URLs para servir media (dev)
  - core/urls.py
  - Adicionar static() para MEDIA_URL
- [X] 13.3 - Criar diretório media/avatars
  - Estrutura de pastas
- [X] 13.4 - Implementar validação de imagem
  - Tamanho máximo (2MB)
  - Formatos permitidos (jpg, png)
  - Mensagens de erro
- [X] 13.5 - Criar placeholder para avatar padrão
  - Imagem ou ícone SVG
  - Exibir quando sem avatar

---

### Sprint 3 - Contas Bancárias (Semana 4)

#### Tarefa 14: Modelo de Account
- [X] 14.1 - Criar Account model
  - accounts/models.py
  - Campo user (ForeignKey)
  - Campo name (CharField)
  - Campo account_type (CharField com choices)
  - Campo initial_balance (DecimalField)
  - Campo current_balance (DecimalField)
  - Campo is_active (BooleanField)
  - Campos created_at e updated_at
  - Método __str__
- [X] 14.2 - Definir choices para account_type
  - CHECKING = 'checking'
  - SAVINGS = 'savings'
  - INVESTMENT = 'investment'
  - OTHER = 'other'
  - Labels em português
- [X] 14.3 - Adicionar Meta class
  - ordering = ['name']
  - verbose_name em português
- [X] 14.4 - Criar e aplicar migrations
  - makemigrations accounts
  - migrate accounts
- [X] 14.5 - Registrar no admin
  - accounts/admin.py
  - list_display, list_filter, search_fields

#### Tarefa 15: Forms de Account
- [X] 15.1 - Criar AccountForm
  - accounts/forms.py
  - ModelForm do Account
  - Campos: name, account_type, initial_balance
  - Widgets customizados
  - Labels e help_texts em português
- [X] 15.2 - Customizar widget de account_type
  - Select estilizado
  - Opções traduzidas
- [X] 15.3 - Validações customizadas
  - Nome obrigatório
  - Initial balance pode ser negativo
  - Mensagens de erro em português

#### Tarefa 16: Views de Account
- [X] 16.1 - Criar AccountListView
  - accounts/views.py
  - ListView
  - Filtrar por user = request.user
  - LoginRequiredMixin
  - Ordenar por nome
- [X] 16.2 - Criar AccountCreateView
  - CreateView
  - Associar user automaticamente
  - Set current_balance = initial_balance
  - Success message
  - Redirect para list
- [X] 16.3 - Criar AccountUpdateView
  - UpdateView
  - Verificar propriedade (user)
  - Não permitir editar initial_balance
  - Success message
- [X] 16.4 - Criar AccountDeleteView
  - DeleteView
  - Verificar propriedade
  - Confirmação
  - Success message
  - Redirect para list
- [X] 16.5 - Criar AccountDetailView (opcional)
  - DetailView
  - Exibir detalhes completos
  - Listar transações da conta

#### Tarefa 17: Templates de Account
- [X] 17.1 - Criar estrutura templates accounts
  - templates/accounts/
- [X] 17.2 - Criar account_list.html
  - Lista em cards ou tabela
  - Saldo total destacado
  - Botão "Nova Conta"
  - Ações: editar, excluir
  - Empty state
- [X] 17.3 - Criar account_form.html
  - Formulário de criação/edição
  - Reutilizável para create e update
  - Estilizado com TailwindCSS
- [X] 17.4 - Criar account_confirm_delete.html
  - Modal ou página de confirmação
  - Avisos se houver transações
  - Botões confirmar/cancelar
- [X] 17.5 - Adicionar no menu
  - Link "Contas" na navbar
  - Destacar quando ativo

#### Tarefa 18: URLs de Account
- [X] 18.1 - Criar accounts/urls.py
  - Padrão RESTful
  - accounts/ (list)
  - accounts/create/ (create)
  - accounts/<pk>/ (detail)
  - accounts/<pk>/edit/ (update)
  - accounts/<pk>/delete/ (delete)
- [X] 18.2 - Incluir em core/urls.py
  - path('accounts/', include('accounts.urls'))

---

### Sprint 4 - Categorias (Semana 5)

#### Tarefa 19: Modelo de Category
- [X] 19.1 - Criar Category model
  - categories/models.py
  - Campo user (ForeignKey)
  - Campo name (CharField)
  - Campo category_type (CharField com choices)
  - Campo color (CharField para hex color)
  - Campo is_default (BooleanField)
  - Campos created_at e updated_at
  - Método __str__
- [X] 19.2 - Definir choices para category_type
  - INCOME = 'income'
  - EXPENSE = 'expense'
  - Labels em português
- [X] 19.3 - Criar constraint de unicidade
  - unique_together = ['user', 'name']
- [X] 19.4 - Criar e aplicar migrations
  - makemigrations categories
  - migrate categories
- [X] 19.5 - Registrar no admin
  - categories/admin.py
  - list_display com cor visual
  - list_filter por tipo

#### Tarefa 20: Categorias Padrão
- [X] 20.1 - Criar management command
  - categories/management/commands/
  - create_default_categories.py
- [X] 20.2 - Implementar lógica do comando
  - Listar categorias padrão
  - Definir cores para cada uma
  - Criar se não existir
  - Marcar is_default=True
- [X] 20.3 - Definir categorias de receita
  - Salário (#10b981)
  - Freelance (#3b82f6)
  - Investimentos (#8b5cf6)
  - Outros (#6b7280)
- [X] 20.4 - Definir categorias de despesa
  - Alimentação (#ef4444)
  - Transporte (#f59e0b)
  - Moradia (#06b6d4)
  - Saúde (#ec4899)
  - Lazer (#14b8a6)
  - Educação (#6366f1)
  - Outros (#6b7280)
- [X] 20.5 - Integrar comando ao signal de criação de usuário
  - Executar ao criar novo usuário
  - profiles/signals.py

#### Tarefa 21: Forms de Category
- [X] 21.1 - Criar CategoryForm
  - categories/forms.py
  - ModelForm do Category
  - Campos: name, category_type, color
  - Excluir is_default
- [X] 21.2 - Implementar color picker
  - Input type="color"
  - Estilização customizada
  - Valor padrão
- [X] 21.3 - Validação de nome único
  - Por usuário
  - Mensagem de erro clara
- [X] 21.4 - Prevenir edição de categorias padrão
  - Verificação no form
  - Ou desabilitar campos

#### Tarefa 22: Views de Category
- [X] 22.1 - Criar CategoryListView
  - categories/views.py
  - Separar receitas e despesas
  - Filtrar por user
  - LoginRequiredMixin
- [X] 22.2 - Criar CategoryCreateView
  - Associar user automaticamente
  - is_default = False
  - Success message
- [X] 22.3 - Criar CategoryUpdateView
  - Verificar propriedade
  - Não permitir editar is_default=True
  - Success message
- [X] 22.4 - Criar CategoryDeleteView
  - Verificar se tem transações
  - Não permitir deletar is_default=True
  - Confirmação
  - Success message
- [X] 22.5 - Adicionar validação de transações vinculadas
  - Query para verificar
  - Mensagem de erro se houver

#### Tarefa 23: Templates de Category
- [X] 23.1 - Criar templates/categories/
- [X] 23.2 - Criar category_list.html
  - Duas colunas: Receitas | Despesas
  - Cards com cor da categoria
  - Badge "Padrão" para is_default
  - Ações: editar, excluir (se permitido)
  - Botão "Nova Categoria"
- [X] 23.3 - Criar category_form.html
  - Formulário com color picker
  - Radio buttons para tipo
  - Preview da cor selecionada
- [X] 23.4 - Criar category_confirm_delete.html
  - Avisos apropriados
  - Verificação de transações
- [X] 23.5 - Adicionar no menu
  - Link "Categorias"

#### Tarefa 24: URLs de Category
- [X] 24.1 - Criar categories/urls.py
  - categories/ (list)
  - categories/create/
  - categories/<pk>/edit/
  - categories/<pk>/delete/
- [X] 24.2 - Incluir em core/urls.py

---

### Sprint 5 - Transações (Semana 6-7)

#### Tarefa 25: Modelo de Transaction
- [X] 25.1 - Criar Transaction model
  - transactions/models.py
  - Campo user (ForeignKey)
  - Campo account (ForeignKey)
  - Campo category (ForeignKey)
  - Campo description (CharField)
  - Campo amount (DecimalField, positivo)
  - Campo transaction_date (DateField)
  - Campo transaction_type (CharField com choices)
  - Campos created_at e updated_at
  - Método __str__
- [X] 25.2 - Definir choices para transaction_type
  - INCOME = 'income'
  - EXPENSE = 'expense'
- [X] 25.3 - Adicionar Meta class
  - ordering = ['-transaction_date', '-created_at']
  - indexes para queries comuns
- [X] 25.4 - Criar e aplicar migrations
  - makemigrations transactions
  - migrate transactions
- [X] 25.5 - Registrar no admin
  - list_display, list_filter, date_hierarchy

#### Tarefa 26: Signals para Atualização de Saldo
- [X] 26.1 - Criar transactions/signals.py
- [X] 26.2 - Signal post_save para Transaction
  - Calcular impacto no saldo
  - Se income: account.current_balance += amount
  - Se expense: account.current_balance -= amount
  - Salvar account
- [X] 26.3 - Signal pre_save para edição
  - Calcular diferença
  - Estornar valor antigo
  - Aplicar valor novo
- [X] 26.4 - Signal post_delete para Transaction
  - Estornar valor da transação
  - Atualizar saldo da conta
- [X] 26.5 - Configurar signal em apps.py
  - transactions/apps.py
  - Importar signals

#### Tarefa 27: Forms de Transaction
- [X] 27.1 - Criar TransactionForm
  - transactions/forms.py
  - ModelForm do Transaction
  - Campos: description, amount, transaction_date, transaction_type, category, account
- [X] 27.2 - Filtrar categorias por tipo
  - JavaScript ou lógica no form
  - Ao selecionar tipo, filtrar categorias
- [X] 27.3 - Filtrar contas do usuário
  - Apenas contas ativas
  - Do usuário logado
- [X] 27.4 - Widgets customizados
  - Date picker
  - Input de valor formatado
  - Select estilizado
- [X] 27.5 - Validações
  - Valor positivo
  - Data não futura (opcional)
  - Campos obrigatórios

#### Tarefa 28: Views de Transaction
- [X] 28.1 - Criar TransactionListView
  - transactions/views.py
  - ListView com paginação (20 items)
  - Filtrar por user
  - LoginRequiredMixin
  - Ordenar por data desc
- [X] 28.2 - Criar TransactionCreateView
  - CreateView
  - Associar user automaticamente
  - Data padrão = hoje
  - Success message
  - Redirect para list
- [X] 28.3 - Criar TransactionUpdateView
  - UpdateView
  - Verificar propriedade
  - Success message
- [X] 28.4 - Criar TransactionDeleteView
  - DeleteView
  - Confirmação
  - Success message
- [X] 28.5 - Criar TransactionDetailView (opcional)
  - DetailView
  - Exibir todos os detalhes

#### Tarefa 29: Filtros de Transaction
- [X] 29.1 - Criar TransactionFilterForm
  - forms.py
  - Campos: date_from, date_to, transaction_type, category, account
  - Todos opcionais
- [X] 29.2 - Implementar filtros na ListView
  - Obter parâmetros GET
  - Aplicar filtros na queryset
  - Passar form para template
- [X] 29.3 - Calcular totais filtrados
  - Total de receitas
  - Total de despesas
  - Saldo (receitas - despesas)
  - Passar para context
- [X] 29.4 - Preservar filtros na URL
  - Query params
  - Pagination com filtros
- [X] 29.5 - Botão "Limpar Filtros"
  - Remover todos os params
  - Voltar à lista completa

#### Tarefa 30: Templates de Transaction
- [X] 30.1 - Criar templates/transactions/
- [X] 30.2 - Criar transaction_list.html
  - Formulário de filtros no topo
  - Cards de totais (receitas, despesas, saldo)
  - Tabela de transações
  - Receitas em verde, despesas em vermelho
  - Paginação
  - Empty state
  - Botão "Nova Transação"
- [X] 30.3 - Criar transaction_form.html
  - Formulário completo
  - JavaScript para filtro de categorias
  - Date picker
  - Validações visuais
- [X] 30.4 - Criar transaction_confirm_delete.html
  - Confirmação com detalhes
  - Avisar sobre impacto no saldo
- [X] 30.5 - Adicionar no menu
  - Link "Transações"

#### Tarefa 31: URLs de Transaction
- [X] 31.1 - Criar transactions/urls.py
  - transactions/ (list com filtros)
  - transactions/create/
  - transactions/<pk>/
  - transactions/<pk>/edit/
  - transactions/<pk>/delete/
- [X] 31.2 - Incluir em core/urls.py

#### Tarefa 32: JavaScript para Filtros Dinâmicos
- [X] 32.1 - Criar static/js/transactions.js
- [X] 32.2 - Implementar filtro de categoria por tipo
  - Listener no campo transaction_type
  - Filtrar options do select de categoria
  - Show/hide baseado no tipo
- [X] 32.3 - Implementar date picker
  - Usar input type="date"
  - Ou biblioteca leve se necessário
- [X] 32.4 - Validação de valor numérico
  - Aceitar apenas números e vírgula/ponto
  - Formatar em tempo real
- [X] 32.5 - Incluir script nos templates

---

### Sprint 6 - Dashboard (Semana 8)

#### Tarefa 33: View do Dashboard
- [X] 33.1 - Criar DashboardView
  - Criar app 'dashboard' ou usar em core
  - TemplateView
  - LoginRequiredMixin
- [X] 33.2 - Implementar cálculo de saldo total
  - Somar current_balance de todas as contas ativas
  - Do usuário logado
- [X] 33.3 - Implementar cálculo de receitas do período
  - Filtrar transações type=income
  - Por período selecionado
  - Somar amounts
- [X] 33.4 - Implementar cálculo de despesas do período
  - Filtrar transações type=expense
  - Por período selecionado
  - Somar amounts
- [X] 33.5 - Calcular saldo do período
  - receitas - despesas
- [X] 33.6 - Buscar últimas 5 transações
  - Ordenar por data desc
  - Limitar a 5
- [X] 33.7 - Calcular resumo por categoria
  - Top 5 categorias com mais despesas
  - Agrupar e somar
- [X] 33.8 - Implementar seletor de período
  - Mês atual (padrão)
  - Mês anterior
  - Últimos 3 meses
  - Ano atual
  - Período customizado

#### Tarefa 34: Template do Dashboard
- [X] 34.1 - Criar templates/dashboard/
- [X] 34.2 - Criar dashboard.html
  - Estrutura com grid responsivo
  - 4 cards de métricas principais
  - Seletor de período
- [X] 34.3 - Cards de métricas
  - Saldo Total (gradiente verde/azul)
  - Receitas do Período (verde)
  - Despesas do Período (vermelho)
  - Saldo do Período (azul/roxo)
  - Valores formatados em R$
- [X] 34.4 - Seção de últimas transações
  - Lista estilizada
  - Link "Ver todas"
- [X] 34.5 - Seção de resumo por categoria
  - Cards ou barras
  - Cores das categorias
  - Percentuais
- [ ] 34.6 - Adicionar gráfico simples (opcional)
  - Chart.js via CDN
  - Gráfico de pizza ou barras
  - Receitas vs Despesas
- [X] 34.7 - Responsividade
  - Mobile: cards em coluna
  - Tablet: 2 colunas
  - Desktop: 4 colunas

#### Tarefa 35: URLs e Navegação
- [X] 35.1 - Criar URL do dashboard
  - dashboard/ ou home/
  - Incluir em core/urls.py
- [ ] 35.2 - Configurar LOGIN_REDIRECT_URL
  - settings.py
  - Apontar para dashboard
- [ ] 35.3 - Configurar LOGOUT_REDIRECT_URL
  - Apontar para landing page
- [ ] 35.4 - Adicionar "Dashboard" no menu
  - Primeiro item da navbar
  - Ícone de home

---

### Sprint 7 - Landing Page Pública (Semana 9)

#### Tarefa 36: View da Landing Page
- [X] 36.1 - Criar LandingPageView
  - core/views.py ou app 'website'
  - TemplateView
  - Acessível sem login
- [X] 36.2 - Verificar se usuário está autenticado
  - Se sim, redirect para dashboard
  - Se não, mostrar landing page

#### Tarefa 37: Template da Landing Page
- [X] 37.1 - Criar templates/landing/
- [X] 37.2 - Criar landing.html
  - Hero section com gradiente
  - Título e subtítulo atrativos
  - CTAs: "Cadastre-se Grátis" e "Entrar"
- [X] 37.3 - Seção de benefícios
  - 3-4 cards com features principais
  - Ícones ou emojis
  - Textos persuasivos
- [X] 37.4 - Seção de como funciona
  - Passos numerados
  - Descrições curtas
- [X] 37.5 - Footer
  - Nome do projeto
  - Ano
  - Links úteis (futuro)
- [X] 37.6 - Design moderno
  - Gradientes
  - Animações suaves (hover, scroll)
  - Totalmente responsivo
- [X] 37.7 - Otimizar textos
  - Português claro
  - Foco em benefícios
  - Call to action forte

#### Tarefa 38: URLs da Landing Page
- [X] 38.1 - Configurar URL raiz
  - path('', LandingPageView.as_view())
  - core/urls.py
- [X] 38.2 - Testar redirecionamento
  - Usuário logado → dashboard
  - Usuário não logado → landing

---

### Sprint 8 - Navbar e Layout Global (Semana 10)

#### Tarefa 39: Navbar Responsiva
- [X] 39.1 - Criar templates/partials/navbar.html
- [X] 39.2 - Implementar logo/brand
  - Texto "Finanpy" com gradiente
  - Link para home (dashboard se logado)
- [X] 39.3 - Menu desktop
  - Links: Dashboard, Contas, Transações, Categorias
  - Destacar página ativa
  - Dropdown de perfil
- [X] 39.4 - Menu mobile
  - Botão hamburger
  - Sidebar ou dropdown
  - Mesmos links do desktop
- [X] 39.5 - Dropdown de usuário
  - Nome do usuário
  - Avatar (se tiver)
  - Link "Meu Perfil"
  - Link "Sair"
- [X] 39.6 - JavaScript para menu mobile
  - Toggle sidebar
  - Close ao clicar fora
  - static/js/navbar.js
- [X] 39.7 - Sticky navbar
  - Fixed no topo
  - Backdrop blur
  - Sombra ao scroll

#### Tarefa 40: Base Template Refinamento
- [X] 40.1 - Atualizar base.html
  - Incluir navbar
  - Incluir messages
  - Estrutura de container
- [X] 40.2 - Criar partial de footer
  - templates/partials/footer.html
  - Informações básicas
  - Simples e discreto
- [X] 40.3 - Configurar blocks
  - {% block title %}
  - {% block content %}
  - {% block extra_css %}
  - {% block extra_js %}
- [X] 40.4 - Adicionar meta tags
  - Viewport
  - Description
  - Charset UTF-8
- [X] 40.5 - Favicon
  - Criar ou usar emoji
  - Adicionar no base.html

#### Tarefa 41: Consistência Visual
- [X] 41.1 - Revisar todos os templates
  - Verificar uso consistente de cores
  - Verificar espaçamentos
  - Verificar tipografia
- [X] 41.2 - Padronizar botões
  - Primário, secundário, danger
  - Tamanhos consistentes
  - Estados hover/active
- [X] 41.3 - Padronizar cards
  - Mesmo estilo em todo sistema
  - Padding e borders iguais
  - Efeitos hover
- [X] 41.4 - Padronizar formulários
  - Mesmos inputs em todos os forms
  - Mensagens de erro no mesmo lugar
  - Botões alinhados
- [X] 41.5 - Criar componentes reutilizáveis
  - templates/components/button.html
  - templates/components/card.html
  - templates/components/form_field.html

---

### Sprint 9 - Polimento e UX (Semana 11)

#### Tarefa 42: Melhorias de UX
- [X] 42.1 - Implementar confirmações de exclusão
  - Modals com SweetAlert2 ou nativo
  - Textos claros de confirmação
- [X] 42.2 - Melhorar feedback de ações
  - Mensagens de sucesso mais visíveis
  - Duração adequada (3-5s)
  - Posição consistente
- [X] 42.3 - Loading states
  - Spinner ao submeter forms
  - Skeleton screens em listas
  - Desabilitar botões durante submit
- [X] 42.4 - Validações em tempo real
  - JavaScript para validar antes de submit
  - Feedback visual imediato
  - Mensagens claras
- [X] 42.5 - Tooltips e hints
  - Explicações em campos complexos
  - Ícones de ajuda
  - Instruções contextuais

#### Tarefa 43: Acessibilidade
- [X] 43.1 - Adicionar labels adequados
  - Todos os inputs com label
  - For/id corretos
- [X] 43.2 - ARIA labels onde necessário
  - Botões sem texto
  - Ícones
  - Navegação
- [X] 43.3 - Contraste de cores
  - Verificar WCAG AA
  - Ajustar se necessário
- [X] 43.4 - Navegação por teclado
  - Tab order lógico
  - Focus visível
  - Atalhos (futuro)
- [X] 43.5 - Textos alternativos
  - Alt em imagens
  - Title em links/botões

#### Tarefa 44: Performance
- [X] 44.1 - Otimizar queries
  - select_related para ForeignKeys
  - prefetch_related para M2M
  - Apenas campos necessários
- [X] 44.2 - Adicionar índices
  - Campos mais consultados
  - created_at, transaction_date
- [X] 44.3 - Paginação eficiente
  - Limit/offset
  - Não carregar tudo
- [X] 44.4 - Otimizar CSS com django-tailwind
  - TailwindCSS já vem configurado com purge
  - Verificar content paths em tailwind.config.js
  - Build para produção: `python manage.py tailwind build`
  - Apenas classes usadas serão incluídas
- [X] 44.5 - Lazy loading de imagens
  - Avatares
  - Imagens grandes (futuro)

#### Tarefa 45: Responsividade
- [X] 45.1 - Testar em mobile (375px)
  - Todos os templates
  - Ajustar breakpoints
- [X] 45.2 - Testar em tablet (768px)
  - Layout intermediário
  - Navegação adequada
- [X] 45.3 - Testar em desktop (1024px+)
  - Uso de espaço
  - Grid layouts
- [X] 45.4 - Testar em diferentes navegadores
  - Chrome, Firefox, Safari, Edge
  - Versões recentes
- [X] 45.5 - Ajustar problemas encontrados
  - CSS fixes
  - JavaScript compatibilidade

---

### Sprint 10 - Refinamentos Finais (Semana 12)

#### Tarefa 46: Formatação de Valores
- [ ] 46.1 - Criar template filter para moeda
  - templatetags/currency_filters.py
  - Formato: R$ 1.234,56
- [ ] 46.2 - Aplicar em todos os valores
  - Dashboard
  - Listas de transações
  - Contas
- [ ] 46.3 - Formatar datas
  - Formato brasileiro: dd/mm/yyyy
  - Templates filters
- [ ] 46.4 - Formatar números grandes
  - Separador de milhares
  - Casas decimais consistentes

#### Tarefa 47: Validações Adicionais
- [ ] 47.1 - Validar deleção de conta com transações
  - Prevenir ou oferecer migração
  - Mensagem clara
- [ ] 47.2 - Validar deleção de categoria em uso
  - Contar transações
  - Bloquear ou sugerir alternativa
- [ ] 47.3 - Validar valores negativos
  - Apenas em campos apropriados
  - Mensagens contextuais
- [ ] 47.4 - Validar datas futuras
  - Permitir ou não (decisão de negócio)
  - Feedback claro

#### Tarefa 48: Documentação
- [ ] 48.1 - Atualizar README.md
  - Descrição completa
  - Features implementadas
  - Screenshots (opcional)
- [ ] 48.2 - Instruções de instalação
  - Passo a passo
  - Requisitos
  - Comandos necessários
- [ ] 48.3 - Documentar estrutura do projeto
  - Apps e responsabilidades
  - Modelos principais
- [ ] 48.4 - Criar CHANGELOG.md
  - Versão 1.0.0
  - Features implementadas
- [ ] 48.5 - Docstrings em código
  - Views principais
  - Models
  - Forms customizados

#### Tarefa 49: Deploy Preparation
- [ ] 49.1 - Configurar variáveis de ambiente
  - python-decouple
  - .env.example
  - SECRET_KEY, DEBUG, ALLOWED_HOSTS
- [ ] 49.2 - Build de produção do Tailwind
  - `python manage.py tailwind build`
  - CSS otimizado e minificado
- [ ] 49.3 - Configurar arquivos estáticos para produção
  - STATIC_ROOT
  - `python manage.py collectstatic`
- [ ] 49.4 - Configurar HTTPS
  - SECURE_SSL_REDIRECT
  - SESSION_COOKIE_SECURE
  - CSRF_COOKIE_SECURE
- [ ] 49.5 - Configurar ALLOWED_HOSTS
  - Domínios permitidos
- [ ] 49.6 - Criar requirements.txt
  - Freeze dependencies
  - Versões específicas

#### Tarefa 50: Testes Finais
- [ ] 50.1 - Teste completo de cadastro
  - Novo usuário
  - Perfil criado
  - Categorias padrão
  - Redirect correto
- [ ] 50.2 - Teste de fluxo de transação
  - Criar conta
  - Criar transação
  - Verificar saldo
  - Editar transação
  - Verificar saldo atualizado
- [ ] 50.3 - Teste de filtros
  - Aplicar múltiplos filtros
  - Verificar resultados
  - Limpar filtros
- [ ] 50.4 - Teste de dashboard
  - Verificar cálculos
  - Trocar período
  - Verificar atualização
- [ ] 50.5 - Teste de validações
  - Tentar criar dados inválidos
  - Verificar mensagens de erro
  - Verificar prevenção

---

### Sprint 11 - Testes Automatizados (Futuro)

#### Tarefa 51: Setup de Testes
- [ ] 51.1 - Configurar pytest-django
  - Instalar pytest
  - pytest-django
  - pytest-cov
- [ ] 51.2 - Criar pytest.ini
  - Configurações
  - DJANGO_SETTINGS_MODULE
- [ ] 51.3 - Criar conftest.py
  - Fixtures compartilhadas
  - User fixture
  - Account fixture
- [ ] 51.4 - Estrutura de testes
  - tests/ em cada app
  - test_models.py
  - test_views.py
  - test_forms.py

#### Tarefa 52: Testes de Models
- [ ] 52.1 - Testes de User
  - Criação de usuário
  - Email único
  - Senha hash
- [ ] 52.2 - Testes de Profile
  - Signal de criação
  - Update de campos
- [ ] 52.3 - Testes de Account
  - Criação
  - Validações
  - Métodos
- [ ] 52.4 - Testes de Category
  - Criação
  - Unicidade por usuário
- [ ] 52.5 - Testes de Transaction
  - Criação
  - Signal de saldo
  - Validações

#### Tarefa 53: Testes de Views
- [ ] 53.1 - Testes de autenticação
  - Signup
  - Login
  - Logout
- [ ] 53.2 - Testes de Account views
  - List, Create, Update, Delete
  - Permissões
- [ ] 53.3 - Testes de Transaction views
  - CRUD completo
  - Filtros
- [ ] 53.4 - Testes de Dashboard
  - Cálculos corretos
  - Permissões

#### Tarefa 54: Testes de Forms
- [ ] 54.1 - Validações de forms
  - Dados válidos
  - Dados inválidos
  - Mensagens de erro
- [ ] 54.2 - Tests de limpeza
  - Clean methods
  - Validações customizadas

#### Tarefa 55: Coverage
- [ ] 55.1 - Configurar coverage
  - .coveragerc
  - Exclusões
- [ ] 55.2 - Rodar coverage
  - pytest --cov
  - Gerar relatório
- [ ] 55.3 - Meta de coverage
  - > 80% inicial
  - > 90% ideal

---

### Sprint 12 - Docker e Deploy (Futuro)

#### Tarefa 56: Dockerfile
- [ ] 56.1 - Criar Dockerfile
  - Base Python 3.10
  - Instalar dependências
  - Copy código
  - CMD para runserver
- [ ] 56.2 - Criar .dockerignore
  - venv/
  - __pycache__/
  - *.pyc
  - db.sqlite3
- [ ] 56.3 - Testar build
  - docker build
  - docker run
  - Verificar funcionamento

#### Tarefa 57: Docker Compose
- [ ] 57.1 - Criar docker-compose.yml
  - Service web
  - Volumes
  - Ports
- [ ] 57.2 - Configurar variáveis
  - Environment
  - .env file
- [ ] 57.3 - Testar compose
  - docker-compose up
  - Migrations
  - Collectstatic

#### Tarefa 58: Deploy em Servidor
- [ ] 58.1 - Escolher plataforma
  - Railway, Render, Heroku
  - VPS (futuro)
- [ ] 58.2 - Configurar servidor
  - Variáveis de ambiente
  - Banco de dados
  - Arquivos estáticos
- [ ] 58.3 - Deploy inicial
  - Push código
  - Migrations
  - Superuser
- [ ] 58.4 - Configurar domínio
  - DNS
  - SSL/HTTPS
- [ ] 58.5 - Monitoramento
  - Logs
  - Erros
  - Performance

---
