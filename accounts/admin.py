from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'account_type', 'current_balance', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active', 'created_at']
    search_fields = ['name', 'user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['user', 'name']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'name', 'account_type', 'is_active')
        }),
        ('Saldo', {
            'fields': ('initial_balance', 'current_balance')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
