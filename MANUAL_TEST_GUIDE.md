# Guia de Testes Manuais - Tarefa 47

Este guia permite que você execute manualmente os testes das validações implementadas na Tarefa 47.

## Credenciais de Teste

```
Email: teste@finanpy.com
Senha: TesteSenha123!
```

## Preparação do Ambiente

O usuário de teste já foi criado com:
- 1 conta bancária: "Conta Teste" (R$ 1.000,00)
- 5 categorias padrão (Alimentação, Transporte, Moradia, Salário, Freelance)

---

## Teste 1: Deleção de Conta COM Transações

### Objetivo
Verificar se o aviso vermelho aparece ao tentar deletar conta com transações.

### Passos
1. Acesse http://localhost:8000/users/login/
2. Faça login com as credenciais de teste
3. Vá para "Contas" no menu
4. Crie uma nova conta:
   - Nome: "Conta para Deletar"
   - Tipo: Conta Corrente
   - Saldo inicial: R$ 500,00
5. Vá para "Transações" no menu
6. Crie uma nova transação:
   - Descrição: "Teste de deleção"
   - Valor: R$ 50,00
   - Data: Hoje
   - Tipo: Despesa
   - Categoria: Alimentação
   - Conta: "Conta para Deletar"
7. Volte para "Contas"
8. Clique em "Excluir" na conta "Conta para Deletar"

### Resultado Esperado
✅ Você deve ver:
- Título vermelho "Excluir Conta"
- Contador mostrando "1 transação"
- Box vermelho de aviso crítico com texto:
  - "Esta conta possui 1 transação vinculada"
  - "TODAS as 1 transação serão permanentemente removidas"
- Botões "Cancelar" e "Sim, Excluir Conta"

### Screenshot Esperado
![Account Delete Warning](https://via.placeholder.com/800x600/1f2937/ef4444?text=Red+Warning+Box)

---

## Teste 2: Deleção de Conta SEM Transações

### Objetivo
Verificar se aparece mensagem verde ao deletar conta vazia.

### Passos
1. Ainda logado, vá para "Contas"
2. Crie uma nova conta:
   - Nome: "Conta Vazia"
   - Tipo: Poupança
   - Saldo inicial: R$ 0,00
3. NÃO crie transações para esta conta
4. Clique em "Excluir" na conta "Conta Vazia"

### Resultado Esperado
✅ Você deve ver:
- Contador mostrando "0" transações
- Box VERDE com ícone de check
- Texto: "Conta Sem Transações"
- Mensagem: "É seguro excluí-la sem perda de dados históricos"
- Botões "Cancelar" e "Sim, Excluir Conta"

---

## Teste 3: Deleção de Categoria COM Transações (BLOQUEADO)

### Objetivo
Verificar se a deleção de categoria com transações é BLOQUEADA.

### Passos
1. Logado no sistema
2. Vá para "Categorias" no menu
3. Crie uma nova categoria personalizada:
   - Nome: "Categoria Teste"
   - Tipo: Despesa
   - Cor: #ff0000 (vermelho)
4. Vá para "Transações"
5. Crie uma transação usando "Categoria Teste"
6. Volte para "Categorias"
7. Tente excluir "Categoria Teste"

### Resultado Esperado
✅ Você deve ver:
- Título: "Exclusão Bloqueada - Transações Vinculadas"
- Box AMARELO com ícone de cadeado
- Texto: "Esta categoria possui X transações vinculadas e não pode ser excluída"
- Lista de instruções:
  - "Reatribuir as transações para outra categoria, ou"
  - "Excluir as transações vinculadas"
- APENAS botão "Voltar para Categorias" (sem botão de confirmar)

---

## Teste 4: Deleção de Categoria SEM Transações (PERMITIDO)

### Objetivo
Verificar se categoria sem transações pode ser deletada.

### Passos
1. Logado no sistema
2. Vá para "Categorias"
3. Crie uma nova categoria:
   - Nome: "Categoria Vazia"
   - Tipo: Receita
   - Cor: #00ff00 (verde)
4. NÃO crie transações para ela
5. Tente excluir "Categoria Vazia"

### Resultado Esperado
✅ Você deve ver:
- Badge verde: "Nenhuma transação"
- Formulário de confirmação COM botões:
  - "Cancelar"
  - "Sim, Excluir Categoria"
- Dica em azul na parte inferior

---

## Teste 5: Tentativa de Deletar Categoria Padrão

### Objetivo
Verificar proteção de categorias padrão.

### Passos
1. Logado no sistema
2. Vá para "Categorias"
3. Tente excluir uma categoria padrão (ex: "Salário" ou "Alimentação")

### Resultado Esperado
✅ Você deve:
- Ver mensagem de erro vermelha (toast/alert no topo)
- Texto: "Categorias padrão não podem ser excluídas"
- Ser redirecionado de volta para lista de categorias
- Categoria NÃO é deletada

---

## Teste 6: Data Futura - Aviso Amarelo (Permitido)

### Objetivo
Verificar que datas futuras mostram AVISO mas permitem criação.

### Passos
1. Logado no sistema
2. Vá para "Transações" → "Nova Transação"
3. Preencha:
   - Descrição: "Transação Futura"
   - Valor: R$ 100,00
   - Data: AMANHÃ (hoje + 1 dia)
   - Tipo: Receita
   - Categoria: Salário
   - Conta: Conta Teste
4. Clique em "Criar Transação"

### Resultado Esperado ANTES de clicar:
✅ Box AMARELO/AMBER aparece abaixo do campo data:
- Ícone de aviso (triângulo)
- Texto: "Nota: Esta transação está agendada para o futuro (amanhã)"
- Fundo: `bg-amber-500/10`
- Borda: `border-amber-500/30`
- Texto: `text-amber-300`

### Resultado Esperado DEPOIS de clicar:
✅ Transação É CRIADA com sucesso
✅ Redirecionamento para lista de transações
✅ Mensagem de sucesso verde

---

## Teste 7: Data Muito Futura - Aviso Forte (Permitido)

### Objetivo
Verificar aviso reforçado para datas muito distantes.

### Passos
1. Nova Transação
2. Preencha com data = hoje + 2 anos (ex: 26/01/2028)
3. Preencha outros campos

### Resultado Esperado
✅ Box AMARELO aparece com texto:
- "Atenção: Esta data está 2.0 anos no futuro"
- "Verifique se a data está correta"
- "Transações futuras são úteis para planejamento, mas datas muito distantes podem ser erros de digitação"

✅ Transação AINDA PODE ser criada (não é bloqueada)

---

## Teste 8: Data Muito Antiga - Erro Vermelho (BLOQUEADO)

### Objetivo
Verificar que datas > 10 anos atrás são BLOQUEADAS.

### Passos
1. Nova Transação
2. Preencha com data = 01/01/2000 (mais de 10 anos atrás)
3. Preencha outros campos
4. Tente criar

### Resultado Esperado
✅ Mensagem de ERRO VERMELHO aparece:
- Texto: "A data da transação não pode ser anterior a 10 anos atrás. Verifique se a data está correta."
- Cor do texto: `text-red-400`
- Formulário NÃO pode ser submetido
- Transação NÃO é criada

---

## Teste 9: Valor Negativo - BLOQUEADO

### Objetivo
Verificar que valores negativos são bloqueados.

### Passos
1. Nova Transação
2. Preencha valor = -100.00
3. Preencha outros campos
4. Tente criar

### Resultado Esperado
✅ Mensagem de ERRO VERMELHO:
- "O valor deve ser maior que zero"
- "Informe apenas valores positivos"
- "O tipo da transação (receita ou despesa) determina como o valor afeta o saldo"
- Formulário é bloqueado

---

## Teste 10: Valor Zero - BLOQUEADO

### Objetivo
Verificar que valor zero é bloqueado.

### Passos
1. Nova Transação
2. Preencha valor = 0.00
3. Tente criar

### Resultado Esperado
✅ Mesma mensagem de erro do valor negativo
✅ Formulário bloqueado

---

## Verificação de Design System

### Cores para Verificar

#### Erros (Vermelho)
- Background: Deve ser vermelho MUITO claro (quase transparente)
- Borda: Vermelho médio com transparência
- Texto: Vermelho claro/médio legível

#### Avisos (Amarelo/Amber)
- Background: Amarelo MUITO claro (quase transparente)
- Borda: Amarelo médio com transparência
- Texto: Amarelo claro legível

#### Sucesso (Verde)
- Background: Verde MUITO claro (quase transparente)
- Borda: Verde médio com transparência
- Texto: Verde claro legível

### Responsividade

Teste em diferentes tamanhos:
1. Mobile (375px): Botões devem empilhar verticalmente
2. Tablet (768px): Layout intermediário
3. Desktop (1920px): Layout completo

---

## Checklist Final

Após executar todos os testes, verifique:

- [ ] Account deletion COM transações mostra warning vermelho
- [ ] Account deletion SEM transações mostra mensagem verde
- [ ] Category deletion COM transações é BLOQUEADA (amarelo)
- [ ] Category deletion SEM transações é PERMITIDA
- [ ] Categorias padrão não podem ser deletadas
- [ ] Data futura mostra AVISO amarelo mas permite criação
- [ ] Data muito futura mostra aviso reforçado
- [ ] Data > 10 anos atrás mostra ERRO e bloqueia
- [ ] Valor negativo é bloqueado com erro
- [ ] Valor zero é bloqueado com erro
- [ ] Todas as cores seguem o design system dark theme
- [ ] Todos os ícones aparecem corretamente
- [ ] Layout responsivo funciona em mobile/tablet/desktop
- [ ] Mensagens em português estão corretas
- [ ] Pluralização (transação/transações) funciona

---

## Relatório de Bugs

Se encontrar algum bug durante os testes manuais, documente aqui:

### BUG-001: [Título]
- **Severidade:** Critical/High/Medium/Low
- **Página:** /path/to/page
- **Passos:**
  1. ...
  2. ...
- **Esperado:** ...
- **Atual:** ...
- **Screenshot:** [anexar]

---

## Notas

- Este guia complementa o relatório automatizado em `TEST_REPORT_TAREFA_47.md`
- Todos os testes foram verificados por análise de código
- Execute em navegador moderno (Chrome, Firefox, Safari, Edge)
- Certifique-se que o servidor está rodando em http://localhost:8000

---

**Boa testagem!**
