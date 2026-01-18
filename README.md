# Finanpy

Finanpy is a personal finance management web application built with Django and TailwindCSS. It allows users to track income/expenses, manage bank accounts, and categorize transactions with a modern, dark-themed interface.

## Features

- User authentication with email-based login
- Personal profile management with avatar support
- Multiple bank account management (checking, savings, investment)
- Transaction tracking with categories
- Dashboard with financial overview
- Dark mode theme with purple/blue gradients
- Responsive design

## Tech Stack

- **Backend:** Python 3.13+, Django 6+
- **Database:** SQLite (development)
- **Frontend:** TailwindCSS 4 via django-tailwind
- **Hot Reload:** django-browser-reload

## Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd finanpy
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

5. Install TailwindCSS dependencies:
```bash
python manage.py tailwind install
```

6. Apply migrations:
```bash
python manage.py migrate
```

7. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

## Development

### Running the Application

You need to run two terminals for development:

**Terminal 1 - Django server:**
```bash
python manage.py runserver
```

**Terminal 2 - TailwindCSS watcher (for hot reload):**
```bash
python manage.py tailwind start
```

The application will be available at http://127.0.0.1:8000

### Main Commands

| Command | Description |
|---------|-------------|
| `python manage.py runserver` | Start Django development server |
| `python manage.py tailwind start` | Start Tailwind CSS in development mode with hot reload |
| `python manage.py tailwind build` | Build optimized CSS for production |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py makemigrations` | Create new migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py collectstatic` | Collect static files for production |

## Project Structure

```
finanpy/
├── core/           # Django project settings, root URLs
├── users/          # Custom user model (email-based auth)
├── profiles/       # User profile data (name, phone, avatar)
├── accounts/       # Bank accounts (checking, savings, investment)
├── categories/     # Transaction categories (income/expense types)
├── transactions/   # Financial transactions
├── theme/          # TailwindCSS configuration and compiled styles
├── templates/      # Global templates (base, partials)
├── static/         # Static assets (JS, images)
└── docs/           # Project documentation
```

## License

This project is for personal/educational use.
