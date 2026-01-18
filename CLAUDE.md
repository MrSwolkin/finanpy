# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Finanpy is a personal finance management web application built with Django. It allows users to track income/expenses, manage bank accounts, and categorize transactions.

**Stack:** Python 3.13+, Django 6+, SQLite, TailwindCSS (planned via django-tailwind)

**Status:** Early development (Sprint 0 - Initial Configuration)

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Development
python manage.py runserver           # Start dev server at http://127.0.0.1:8000
python manage.py migrate             # Apply migrations
python manage.py makemigrations      # Create new migrations
python manage.py createsuperuser     # Create admin user

# TailwindCSS (after setup)
python manage.py tailwind start      # Dev mode with hot reload
python manage.py tailwind build      # Production build
```

## Architecture

```
finanpy/
├── core/           # Django project settings, root URLs
├── users/          # Custom user model (email-based auth)
├── profiles/       # User profile data (name, phone, avatar)
├── accounts/       # Bank accounts (checking, savings, investment)
├── categories/     # Transaction categories (income/expense types)
├── transactions/   # Financial transactions
└── docs/           # Project documentation
```

**Key relationships:**
- User has one Profile (OneToOne)
- User owns multiple Accounts and Categories (ForeignKey)
- Transaction belongs to Account and Category

## Code Standards

**Language:** Code in English, UI text in Portuguese (pt-BR)

**Style:**
- PEP8 compliant
- Single quotes for strings
- 4-space indentation

**Django patterns:**
- Class-Based Views with mixins (`LoginRequiredMixin`)
- Filter querysets by `user=request.user` for data isolation
- Use `select_related()` / `prefetch_related()` for query optimization

**Commits:** English, conventional format (`feat:`, `fix:`, `refactor:`)

## Frontend (TailwindCSS)

Dark mode theme with purple/blue gradients. See `docs/design-system.md` for component patterns.

**Key colors:**
- Background: `bg-gray-900`, `bg-gray-800`
- Primary gradient: `from-purple-600 to-blue-600`
- Income: `text-green-400`
- Expense: `text-red-400`

## Documentation

Full documentation available in `docs/`:
- `setup.md` - Installation steps
- `architecture.md` - Project structure
- `code-standards.md` - Coding conventions
- `design-system.md` - UI components and colors
- `PRD.md` - Product requirements and task list
