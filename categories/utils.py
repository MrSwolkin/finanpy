"""
Utility functions for the categories app.
"""

from .models import Category


# Default income categories with colors
DEFAULT_INCOME_CATEGORIES = [
    {'name': 'Salário', 'color': '#10b981'},
    {'name': 'Freelance', 'color': '#3b82f6'},
    {'name': 'Investimentos', 'color': '#8b5cf6'},
    {'name': 'Outros', 'color': '#6b7280'},
]

# Default expense categories with colors
DEFAULT_EXPENSE_CATEGORIES = [
    {'name': 'Alimentação', 'color': '#ef4444'},
    {'name': 'Transporte', 'color': '#f59e0b'},
    {'name': 'Moradia', 'color': '#06b6d4'},
    {'name': 'Saúde', 'color': '#ec4899'},
    {'name': 'Lazer', 'color': '#14b8a6'},
    {'name': 'Educação', 'color': '#6366f1'},
    {'name': 'Outros', 'color': '#6b7280'},
]


def create_default_categories_for_user(user):
    """
    Create default income and expense categories for a user.

    Args:
        user: The User instance to create categories for

    Returns:
        tuple: (created_count, existing_count) - number of categories created vs. already existing
    """
    created_count = 0
    existing_count = 0

    # Create income categories
    for cat_data in DEFAULT_INCOME_CATEGORIES:
        _, created = Category.objects.get_or_create(
            user=user,
            name=cat_data['name'],
            defaults={
                'category_type': Category.INCOME,
                'color': cat_data['color'],
                'is_default': True,
            }
        )
        if created:
            created_count += 1
        else:
            existing_count += 1

    # Create expense categories
    for cat_data in DEFAULT_EXPENSE_CATEGORIES:
        _, created = Category.objects.get_or_create(
            user=user,
            name=cat_data['name'],
            defaults={
                'category_type': Category.EXPENSE,
                'color': cat_data['color'],
                'is_default': True,
            }
        )
        if created:
            created_count += 1
        else:
            existing_count += 1

    return created_count, existing_count
