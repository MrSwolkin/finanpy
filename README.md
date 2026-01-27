# Finanpy

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Django](https://img.shields.io/badge/Django-6+-green.svg)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4-06B6D4.svg)
![License](https://img.shields.io/badge/License-Personal%2FEducational-yellow.svg)

**Finanpy** is a personal finance management web application built with Django and TailwindCSS. It provides a modern, dark-themed interface for tracking income/expenses, managing multiple bank accounts, and categorizing financial transactions.

## Features

### User Management
- Email-based authentication (no username required)
- Secure password reset workflow
- Personal profile with avatar upload support
- Automatic login after registration

### Bank Accounts
- Multiple account types: Checking, Savings, Investment, Other
- Real-time balance tracking
- Automatic balance updates via transactions
- Support for negative balances (overdraft scenarios)

### Transaction Tracking
- Income and expense recording
- Automatic account balance updates
- Rich filtering options (date range, type, category, account)
- Future transaction support with smart warnings
- Pagination for large datasets

### Categories
- Custom income/expense categories
- Color-coded for visual identification
- Pre-configured default categories
- Protection against deletion when in use

### Dashboard
- Total balance overview across all accounts
- Period-based analytics (current month, last month, quarterly, yearly)
- Income vs Expense breakdown
- Top expense categories
- Recent transactions quick view

### UI/UX
- Modern dark theme with purple/blue gradients
- Fully responsive design (mobile, tablet, desktop)
- WCAG accessibility compliant
- Portuguese (pt-BR) interface
- Real-time form validation

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.13+, Django 6+ |
| Database | SQLite (development) |
| Frontend | TailwindCSS 4, Django Template Language |
| Hot Reload | django-tailwind, django-browser-reload |
| Environment | python-decouple |

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Node.js (automatically managed by django-tailwind)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd finanpy
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

> **Tip:** Generate a secure SECRET_KEY using:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Install TailwindCSS Dependencies

```bash
python manage.py tailwind install
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Development

### Running the Application

You need **two terminals** for development:

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
```

**Terminal 2 - TailwindCSS Watcher:**
```bash
python manage.py tailwind start
```

The application will be available at **http://127.0.0.1:8000**

### Commands Reference

| Command | Description |
|---------|-------------|
| `python manage.py runserver` | Start Django development server |
| `python manage.py tailwind start` | Start Tailwind with hot reload |
| `python manage.py tailwind build` | Build optimized CSS for production |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py makemigrations` | Create new migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py collectstatic` | Collect static files for production |
| `python manage.py test` | Run test suite |

## Project Structure

```
finanpy/
├── core/               # Django project settings and root URLs
│   ├── settings.py     # Main configuration
│   ├── urls.py         # Root URL routing
│   ├── views.py        # DashboardView
│   └── templatetags/   # Custom template filters (currency, dates)
│
├── users/              # User authentication
│   ├── models.py       # CustomUser model (email-based)
│   ├── views.py        # SignUp, Login, Logout, Password Reset
│   └── forms.py        # User creation and authentication forms
│
├── profiles/           # User profile management
│   ├── models.py       # Profile model (name, phone, avatar)
│   ├── views.py        # ProfileDetail, ProfileUpdate
│   ├── forms.py        # Profile editing form
│   └── signals.py      # Auto-create profile on user creation
│
├── accounts/           # Bank account management
│   ├── models.py       # Account model (types, balances)
│   ├── views.py        # CRUD operations
│   └── forms.py        # Account creation/editing
│
├── categories/         # Transaction categories
│   ├── models.py       # Category model (type, color)
│   ├── views.py        # CRUD with protection logic
│   └── management/     # Default categories command
│
├── transactions/       # Financial transactions
│   ├── models.py       # Transaction model
│   ├── views.py        # CRUD with filtering
│   ├── forms.py        # Transaction form with validation
│   └── signals.py      # Auto-update account balances
│
├── theme/              # TailwindCSS configuration
│   └── static_src/     # Tailwind source files
│
├── templates/          # Global templates
│   ├── base.html       # Base template
│   ├── partials/       # Navbar, footer, messages
│   └── components/     # Reusable UI components
│
├── static/             # Static assets
│   ├── js/             # JavaScript files
│   └── images/         # Image assets
│
├── media/              # User uploads (avatars)
│
└── docs/               # Project documentation
```

## Main Models

### CustomUser (users)
- Email-based authentication
- Extends Django's AbstractUser
- No username field required

### Profile (profiles)
- OneToOne relationship with User
- Fields: first_name, last_name, phone, avatar
- Auto-created via signal on user registration

### Account (accounts)
- Types: checking, savings, investment, other
- Tracks initial_balance and current_balance
- Supports negative balances for overdraft

### Category (categories)
- Types: income, expense
- Color field for visual identification
- Default categories protected from deletion

### Transaction (transactions)
- Links to Account and Category
- Automatic balance updates via signals
- Rich validation (amount > 0, date range checks)

## URL Routes

| Route | Description |
|-------|-------------|
| `/` | Redirects to login |
| `/dashboard/` | Main dashboard with analytics |
| `/signup/` | User registration |
| `/login/` | User login |
| `/logout/` | User logout |
| `/password-reset/` | Password reset flow |
| `/profile/` | View profile |
| `/profile/edit/` | Edit profile |
| `/accounts/` | List accounts |
| `/accounts/create/` | Create account |
| `/categories/` | List categories |
| `/categories/create/` | Create category |
| `/transactions/` | List transactions with filters |
| `/transactions/create/` | Create transaction |
| `/admin/` | Django admin interface |

## Code Standards

- **Language:** Code in English, UI in Portuguese (pt-BR)
- **Style:** PEP8 compliant, 4-space indentation
- **Commits:** Conventional format (`feat:`, `fix:`, `refactor:`)
- **Views:** Class-Based Views with mixins (LoginRequiredMixin)
- **Queries:** Always filtered by `user=request.user` for data isolation

## Documentation

Additional documentation available in `docs/`:

| File | Description |
|------|-------------|
| `architecture.md` | Project structure details |
| `code-standards.md` | Coding conventions |
| `design-system.md` | UI components and colors |
| `setup.md` | Detailed setup instructions |
| `template-filters.md` | Custom template filters |
| `ACCESSIBILITY_IMPROVEMENTS.md` | WCAG compliance notes |

## Testing

Run the test suite:

```bash
python manage.py test
```

Run specific app tests:

```bash
python manage.py test transactions
```

## Production Build

1. Build optimized CSS:
```bash
python manage.py tailwind build
```

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Set environment variables:
```env
DEBUG=False
SECRET_KEY=<secure-production-key>
ALLOWED_HOSTS=your-domain.com
```

## License

This project is for personal/educational use.

---

**Developed with Django and TailwindCSS**
