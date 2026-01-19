# Project Overview

This is a Django-based personal finance management application called Finanpy. It helps users track their income and expenses, manage multiple bank accounts, and categorize their transactions. The frontend is built with TailwindCSS, and the project includes features like user authentication, profile management, and a dark-themed, responsive interface.

## Building and Running

### Prerequisites

- Python 3.10+
- pip

### Setup & Execution

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    Create a `.env` file in the project root with the following content:
    ```env
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    ```

4.  **Set up TailwindCSS:**
    ```bash
    python manage.py tailwind install
    ```

5.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development servers:**

    *   **Terminal 1 (Django):**
        ```bash
        python manage.py runserver
        ```

    *   **Terminal 2 (TailwindCSS):**
        ```bash
        python manage.py tailwind start
        ```
The application will be running at `http://127.0.0.1:8000/`.

### Key Commands

*   `python manage.py runserver`: Starts the Django development server.
*   `python manage.py tailwind start`: Starts the TailwindCSS watcher for hot-reloading.
*   `python manage.py tailwind build`: Builds the optimized CSS for production.
*   `python manage.py migrate`: Applies database migrations.
*   `python manage.py makemigrations`: Creates new database migrations.
*   `python manage.py createsuperuser`: Creates an admin user.
*   `python manage.py collectstatic`: Collects static files for production.

## Development Conventions

*   **Custom User Model:** The project uses a custom user model located in the `users` app (`users.CustomUser`).
*   **Configuration:** The `python-decouple` library is used to manage settings and secrets. Configuration is stored in a `.env` file in the project root.
*   **Frontend:** The frontend is built with TailwindCSS, and the configuration is managed by `django-tailwind`.
*   **Apps:** The project is organized into several Django apps, including `accounts`, `categories`, `profiles`, `transactions`, and `users`.
*   **Database:** The project uses SQLite for development.
*   **Static Files:** Static files are located in the `static` directory, and user-uploaded media files are in the `media` directory.
