# Design System

Sistema de design para interface do Finanpy usando TailwindCSS.

## Paleta de Cores

### Cores Primarias (Gradientes)

| Nome | Classes TailwindCSS |
|------|---------------------|
| Primary | `bg-gradient-to-r from-purple-600 to-blue-600` |
| Secondary | `bg-gradient-to-r from-cyan-500 to-blue-500` |
| Accent | `bg-gradient-to-r from-pink-500 to-purple-600` |

### Cores de Fundo (Modo Escuro)

| Uso | Classe |
|-----|--------|
| Background Principal | `bg-gray-900` |
| Background Secundario | `bg-gray-800` |
| Background Card | `bg-gray-800/50 backdrop-blur-sm` |
| Bordas | `border-gray-700` |

### Cores de Texto

| Uso | Classe |
|-----|--------|
| Texto Principal | `text-gray-100` |
| Texto Secundario | `text-gray-400` |
| Texto Destaque | `text-white` |

### Cores de Status

| Status | Texto | Background |
|--------|-------|------------|
| Sucesso | `text-green-400` | `bg-green-500/10` |
| Erro | `text-red-400` | `bg-red-500/10` |
| Aviso | `text-yellow-400` | `bg-yellow-500/10` |
| Info | `text-blue-400` | `bg-blue-500/10` |

### Cores Funcionais

| Tipo | Texto | Background |
|------|-------|------------|
| Receita | `text-green-400` | `bg-green-500/10` |
| Despesa | `text-red-400` | `bg-red-500/10` |

## Tipografia

**Fonte**: Inter (ou system-ui como fallback)

| Elemento | Classes |
|----------|---------|
| Heading 1 | `text-4xl font-bold` |
| Heading 2 | `text-3xl font-bold` |
| Heading 3 | `text-2xl font-semibold` |
| Heading 4 | `text-xl font-semibold` |
| Body Large | `text-lg` |
| Body | `text-base` |
| Body Small | `text-sm` |
| Caption | `text-xs` |

## Componentes

### Botao Primario

```html
<button class="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl">
    Texto
</button>
```

### Botao Secundario

```html
<button class="px-6 py-3 bg-gray-700 text-gray-100 rounded-lg font-semibold hover:bg-gray-600 transition-all duration-200">
    Texto
</button>
```

### Botao Perigo

```html
<button class="px-6 py-3 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-all duration-200">
    Excluir
</button>
```

### Input

```html
<input type="text"
       class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent transition-all duration-200"
       placeholder="Digite aqui...">
```

### Card

```html
<div class="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-200">
    <h3 class="text-xl font-semibold text-gray-100 mb-2">Titulo</h3>
    <p class="text-gray-400">Conteudo</p>
</div>
```

### Mensagem de Sucesso

```html
<div class="bg-green-500/10 border border-green-500/30 rounded-lg p-4 mb-4">
    <p class="text-green-400 text-sm">Operacao realizada com sucesso!</p>
</div>
```

### Mensagem de Erro

```html
<div class="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-4">
    <p class="text-red-400 text-sm">Ocorreu um erro. Tente novamente.</p>
</div>
```

### Badge Receita

```html
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/30">
    Receita
</span>
```

### Badge Despesa

```html
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-500/10 text-red-400 border border-red-500/30">
    Despesa
</span>
```

## Layout

### Container Principal

```html
<div class="min-h-screen bg-gray-900">
    <!-- Conteudo -->
</div>
```

### Container de Conteudo

```html
<div class="container mx-auto px-4 py-8 max-w-7xl">
    <!-- Conteudo -->
</div>
```

### Grid de Cards

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- Cards -->
</div>
```

### Grid de Dashboard (4 colunas)

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <!-- Cards de metricas -->
</div>
```

## Responsividade

| Breakpoint | Largura | Uso |
|------------|---------|-----|
| sm | 640px | Smartphones grandes |
| md | 768px | Tablets |
| lg | 1024px | Desktops |
| xl | 1280px | Desktops grandes |

## Loading State

```html
<div class="flex items-center justify-center py-12">
    <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
</div>
```

## Empty State

```html
<div class="text-center py-12">
    <h3 class="text-xl font-semibold text-gray-300 mb-2">Nenhum registro encontrado</h3>
    <p class="text-gray-400 mb-6">Comece adicionando seu primeiro item</p>
    <button class="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-semibold">
        Adicionar Agora
    </button>
</div>
```
