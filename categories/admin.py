from django.contrib import admin
from django.utils.html import mark_safe

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""

    list_display = ['name', 'category_type', 'colored_color', 'is_default', 'user', 'created_at']
    list_filter = ['category_type', 'is_default', 'created_at']
    search_fields = ['name', 'user__email']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

    def colored_color(self, obj):
        """Display a visual color square with the category color."""
        return mark_safe(
            f'<div style="width: 20px; height: 20px; background-color: {obj.color}; '
            f'border: 1px solid #ccc; border-radius: 3px;"></div>'
        )
    colored_color.short_description = 'Cor'
