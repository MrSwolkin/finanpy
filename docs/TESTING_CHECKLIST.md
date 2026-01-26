# Checklist de Testes de Responsividade - Finanpy

## Como usar este checklist

Este documento serve como guia rápido para testes manuais de responsividade antes de cada deploy ou após modificações de UI.

---

## Pré-requisitos

- [ ] Servidor rodando em http://localhost:8000
- [ ] Conta de teste criada (teste@finanpy.com / TesteSenha123!)
- [ ] Dados de teste populados (contas, transações, categorias)
- [ ] Chrome DevTools ou Firefox DevTools aberto

---

## Viewports a Testar

### Mobile - 375x667 (iPhone SE)
```javascript
// Chrome DevTools Console
window.resizeTo(375, 667);
```

### Tablet - 768x1024 (iPad)
```javascript
window.resizeTo(768, 1024);
```

### Desktop - 1280x1024
```javascript
window.resizeTo(1280, 1024);
```

---

## Checklist por Página

### 1. Login (/users/login/)

**Mobile (375px)**
- [ ] Logo centralizado e legível
- [ ] Campos de input full-width
- [ ] Botão "Entrar" full-width
- [ ] Link "Esqueceu senha" visível
- [ ] Link "Cadastre-se" visível
- [ ] Padding adequado nas laterais

**Tablet (768px)**
- [ ] Layout mantém centralização
- [ ] Card de login com largura adequada

**Desktop (1280px)**
- [ ] Card centralizado com max-width
- [ ] Whitespace adequado

---

### 2. Dashboard (/dashboard/)

**Mobile (375px)**
- [ ] Menu hamburger aparece no navbar
- [ ] Cards de métricas empilham verticalmente (1 coluna)
- [ ] Seletor de período empilha verticalmente
- [ ] Botão "Filtrar" full-width
- [ ] Transações recentes legíveis
- [ ] Categorias de despesas visíveis
- [ ] Footer empilha verticalmente

**Tablet (768px)**
- [ ] Cards de métricas em 2 colunas
- [ ] Seletor de período em linha horizontal
- [ ] Transações e categorias lado a lado
- [ ] Menu mobile ainda aparece

**Desktop (1280px)**
- [ ] Navegação desktop visível
- [ ] 4 cards de métricas lado a lado
- [ ] Filtros em linha horizontal
- [ ] Layout 2 colunas para transações/categorias
- [ ] Dropdown de usuário funcional

---

### 3. Lista de Transações (/transactions/)

**Mobile (375px)**
- [ ] Botão "Nova Transação" full-width
- [ ] Filtros empilham em coluna única
- [ ] Cards de resumo empilham (3 cards verticais)
- [ ] ⚠️ ISSUE CONHECIDA: Tabela requer scroll horizontal
- [ ] Paginação funciona (pode quebrar linha)
- [ ] Empty state bem formatado

**Tablet (768px)**
- [ ] Filtros em 2 colunas
- [ ] Cards de resumo em 3 colunas lado a lado
- [ ] Tabela mais legível
- [ ] Paginação inline

**Desktop (1280px)**
- [ ] Filtros em 5 colunas
- [ ] Tabela totalmente visível sem scroll
- [ ] Ações (Editar/Excluir) bem espaçadas
- [ ] Paginação completa inline

---

### 4. Lista de Contas (/accounts/)

**Mobile (375px)**
- [ ] Card de saldo total responsivo
- [ ] Cards de conta empilham verticalmente
- [ ] Nome da conta trunca se muito longo
- [ ] ⚠️ ISSUE CONHECIDA: 3 botões muito próximos
- [ ] Botão "Nova Conta" full-width

**Tablet (768px)**
- [ ] Cards de saldo total bem espaçado
- [ ] Cards de conta em 2 colunas
- [ ] Botões de ação com espaço adequado

**Desktop (1280px)**
- [ ] Cards em 3 colunas
- [ ] Layout balanceado
- [ ] Botões bem espaçados

---

### 5. Lista de Categorias (/categories/)

**Mobile (375px)**
- [ ] Cards empilham verticalmente
- [ ] Nome de categoria visível
- [ ] Cor da categoria exibida
- [ ] Botões de ação acessíveis

**Tablet (768px)**
- [ ] Cards em 2 colunas

**Desktop (1280px)**
- [ ] Cards em 3 colunas

---

### 6. Formulários (Create/Edit)

**Mobile (375px)**
- [ ] Todos os campos full-width
- [ ] Labels legíveis
- [ ] Mensagens de erro visíveis
- [ ] Botão de submit full-width
- [ ] Datepicker funcional

**Tablet (768px)**
- [ ] Formulário com largura adequada
- [ ] Campos não muito largos

**Desktop (1280px)**
- [ ] Formulário centralizado
- [ ] Max-width aplicado

---

### 7. Perfil (/profile/)

**Todos os viewports**
- [ ] Avatar visível e responsivo
- [ ] Campos de perfil adaptados
- [ ] Botão de editar acessível

---

## Testes de Interação

### Touch Targets (Mobile)
- [ ] Todos os botões ≥ 44x44px
- [ ] Links do menu ≥ 44px de altura
- [ ] Checkboxes e radios com área clicável adequada
- [ ] Dropdown items espaçados

### Navegação
- [ ] Menu hamburger abre/fecha suavemente
- [ ] Dropdown de usuário funciona
- [ ] Links ativos têm destaque visual
- [ ] Voltar do browser funciona

### Formulários
- [ ] Focus ring visível em todos os campos
- [ ] Tab order lógico
- [ ] Enter submete formulário
- [ ] Validação mostra erros corretamente

---

## Testes de Conteúdo

### Overflow e Truncate
- [ ] Nomes longos de conta truncam com "..."
- [ ] Descrições longas de transação quebram linha adequadamente
- [ ] Emails longos não quebram layout
- [ ] Números grandes formatam corretamente

### Estados Vazios
- [ ] Dashboard sem transações mostra empty state
- [ ] Lista de contas vazia mostra CTA para criar
- [ ] Filtros sem resultados mostram mensagem clara

### Dados Volumosos
- [ ] Lista com 50+ transações pagina corretamente
- [ ] Dashboard com muitas categorias mantém layout
- [ ] Performance não degrada com muitos dados

---

## Testes Cross-Browser

### Chrome
- [ ] Layout correto em todos os viewports
- [ ] Animações suaves
- [ ] Backdrop-blur funciona

### Firefox
- [ ] Layout consistente com Chrome
- [ ] Formulários funcionam
- [ ] backdrop-filter pode não funcionar (OK)

### Safari (se disponível)
- [ ] iOS Safari - viewport correto
- [ ] Desktop Safari - layout OK

### Edge
- [ ] Comportamento similar ao Chrome

---

## Issues Conhecidas (Para referência)

### Alta Prioridade
1. **ISSUE-MOB-001:** Tabela de transações em mobile requer scroll horizontal excessivo
   - Workaround: Use scroll horizontal
   - Fix planejado: Layout de card para mobile

2. **ISSUE-MOB-002:** Botões de ação em cards de conta muito próximos
   - Workaround: Toque com cuidado
   - Fix planejado: Dropdown menu ou stacking

### Média Prioridade
3. **ISSUE-MOB-003:** Paginação pode quebrar linha
4. **ISSUE-COMPAT-001:** backdrop-blur não funciona em navegadores antigos

---

## Lighthouse Audits

### Mobile
```bash
# Chrome DevTools > Lighthouse
# Selecionar: Mobile, Performance, Accessibility, Best Practices
```
- [ ] Performance ≥ 90
- [ ] Accessibility ≥ 90
- [ ] Best Practices ≥ 90
- [ ] SEO ≥ 90

### Desktop
- [ ] Performance ≥ 95
- [ ] Accessibility ≥ 95
- [ ] Best Practices ≥ 95
- [ ] SEO ≥ 95

---

## Quando Usar Este Checklist

✅ **Use antes de:**
- Deploy para produção
- Merge de PR com mudanças de UI
- Release de nova versão
- Modificações significativas de CSS

✅ **Use após:**
- Atualização de TailwindCSS
- Mudanças em templates base
- Modificações no navbar/footer
- Adicionar novos componentes

---

## Ferramentas Úteis

### Chrome DevTools
```
1. F12 para abrir DevTools
2. Ctrl+Shift+M para toggle device mode
3. Selecionar "Responsive" e ajustar dimensões
```

### Firefox DevTools
```
1. F12 para abrir DevTools
2. Ctrl+Shift+M para responsive design mode
3. Selecionar dispositivo ou dimensões customizadas
```

### Comandos de Teste
```bash
# Iniciar servidor
python manage.py runserver

# Em outro terminal - verificar acessibilidade
npx @axe-core/cli http://localhost:8000

# Lighthouse via CLI
lighthouse http://localhost:8000 --view
```

---

## Relatórios Gerados

Após teste completo de responsividade (26/01/2026):
- 📄 **RESPONSIVENESS_TEST_REPORT.md** - Relatório detalhado (791 linhas)
- 📋 **RESPONSIVENESS_ISSUES_SUMMARY.md** - Resumo executivo (91 linhas)

---

## Contato

Para questões sobre testes de responsividade:
- Consultar RESPONSIVENESS_TEST_REPORT.md
- Issues documentadas no GitHub
- Documentação do TailwindCSS: https://tailwindcss.com/docs/responsive-design

---

**Última atualização:** 26 de Janeiro de 2026
**Versão:** 1.0
