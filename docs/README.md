# Finanpy - Documentacao

Documentacao do projeto Finanpy, um sistema de gestao de financas pessoais desenvolvido com Django.

## Indice

| Documento | Descricao |
|-----------|-----------|
| [Setup](setup.md) | Como configurar e rodar o projeto |
| [Arquitetura](architecture.md) | Estrutura e organizacao do projeto |
| [Padroes de Codigo](code-standards.md) | Convencoes e padroes de codigo |
| [Design System](design-system.md) | Paleta de cores e componentes visuais |

## Sobre o Projeto

O Finanpy e uma aplicacao web para gerenciamento financeiro pessoal que permite:

- Controlar receitas e despesas
- Gerenciar multiplas contas bancarias
- Categorizar transacoes
- Visualizar dashboard com resumo financeiro

## Stack Tecnologica

- **Backend**: Python 3.13+, Django 6+
- **Banco de Dados**: SQLite
- **Frontend**: Django Template Language, TailwindCSS (planejado)

## Status Atual

O projeto esta em fase inicial de desenvolvimento (Sprint 0 - Configuracao Inicial).

### Apps Criados

- `users` - Gerenciamento de usuarios
- `profiles` - Perfis de usuario
- `accounts` - Contas bancarias
- `categories` - Categorias de transacoes
- `transactions` - Transacoes financeiras
- `core` - Configuracoes do projeto Django
