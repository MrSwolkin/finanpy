from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction model."""

    list_display = ['description', 'amount', 'transaction_type', 'category', 'account', 'transaction_date', 'user']
    list_filter = ['transaction_type', 'category', 'account', 'user']
    search_fields = ['description']
    date_hierarchy = 'transaction_date'
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-transaction_date', '-created_at']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'description', 'transaction_type')
        }),
        ('Detalhes Financeiros', {
            'fields': ('amount', 'account', 'category', 'transaction_date')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
