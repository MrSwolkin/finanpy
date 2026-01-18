from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model."""
    list_display = ['user', 'first_name', 'last_name', 'phone', 'created_at']
    search_fields = ['user__email', 'first_name', 'last_name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['user']
