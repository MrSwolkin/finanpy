# Agentes de IA - Finanpy

Este diretorio contem os agentes de IA especializados para o desenvolvimento do Finanpy. Cada agente e um especialista em uma area especifica da stack do projeto.

## Stack do Projeto

- **Backend**: Python 3.13+, Django 6+, SQLite
- **Frontend**: Django Template Language, TailwindCSS (via django-tailwind)
- **Testes**: Playwright MCP para testes end-to-end

---

## Indice de Agentes

| Agente | Arquivo | Descricao |
|--------|---------|-----------|
| [Backend Django](#backend-django) | [backend-django.md](backend-django.md) | Especialista em desenvolvimento backend com Django |
| [Frontend TailwindCSS + DTL](#frontend-tailwind-django) | [frontend-tailwind-django.md](frontend-tailwind-django.md) | Especialista em templates Django e TailwindCSS |
| [QA Tester](#qa-tester) | [qa-tester.md](qa-tester.md) | Especialista em testes end-to-end com Playwright |

---

## Backend Django

**Arquivo:** [backend-django.md](backend-django.md)

**Quando usar:**
- Criar ou modificar models Django
- Implementar views (Class-Based Views)
- Criar forms e validacoes
- Configurar URLs e rotas
- Implementar signals
- Criar management commands
- Configurar admin Django
- Otimizar queries (select_related, prefetch_related)
- Implementar autenticacao e permissoes

**MCP Server:** Context7 - para consultar documentacao atualizada do Django 6+

---

## Frontend TailwindCSS + DTL

**Arquivo:** [frontend-tailwind-django.md](frontend-tailwind-django.md)

**Quando usar:**
- Criar templates Django (.html)
- Estilizar componentes com TailwindCSS
- Implementar layouts responsivos
- Criar partials e componentes reutilizaveis
- Implementar formularios estilizados
- Adicionar interatividade com JavaScript vanilla
- Seguir o Design System do projeto (modo escuro, gradientes)

**MCP Server:** Context7 - para consultar documentacao atualizada do TailwindCSS 3.x e Django Templates

---

## QA Tester

**Arquivo:** [qa-tester.md](qa-tester.md)

**Quando usar:**
- Testar fluxos de usuario end-to-end
- Verificar se o design esta correto
- Validar responsividade em diferentes tamanhos de tela
- Testar formularios e validacoes
- Verificar mensagens de erro e sucesso
- Testar autenticacao (login, logout, cadastro)
- Gerar relatorios de bugs e melhorias de UI/UX

**MCP Server:** Playwright - para automacao de testes no navegador

---

## Como Usar os Agentes

### 1. Invocando um Agente

Para usar um agente, utilize o comando Task com o subagent_type apropriado:

```
Task tool com subagent_type correspondente ao agente desejado
```

### 2. Contexto Necessario

Sempre forneça ao agente:
- O arquivo ou funcionalidade especifica a ser trabalhada
- Referencia ao PRD.md para requisitos funcionais
- Referencia ao design-system.md para padroes visuais (frontend)

### 3. Fluxo de Trabalho Recomendado

1. **Backend Django** - Implemente models, views e logica de negocios
2. **Frontend TailwindCSS** - Crie templates e estilizacao
3. **QA Tester** - Valide a implementacao com testes end-to-end

---

## Padroes Compartilhados

Todos os agentes devem seguir:

- **Codigo em ingles**, UI em portugues (pt-BR)
- **PEP8** para Python
- **Aspas simples** para strings
- **Commits** em ingles, formato convencional (`feat:`, `fix:`, `refactor:`)
- **Isolamento de dados** por usuario (`user=request.user`)
- **Design System** do projeto (modo escuro, gradientes purple/blue)
