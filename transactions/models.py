from django.conf import settings
from django.db import models


class Transaction(models.Model):
    """
    Model representing a financial transaction.
    Can be either income or expense type, linked to an account and category.
    """

    # Transaction type choices
    INCOME = 'income'
    EXPENSE = 'expense'

    TRANSACTION_TYPE_CHOICES = [
        (INCOME, 'Receita'),
        (EXPENSE, 'Despesa'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Usuário'
    )
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Conta'
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Categoria'
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Descrição'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor'
    )
    transaction_date = models.DateField(
        verbose_name='Data da Transação'
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='Tipo'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        ordering = ['-transaction_date', '-created_at']
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        indexes = [
            models.Index(fields=['user', 'transaction_date']),
            models.Index(fields=['user', 'transaction_type']),
            models.Index(fields=['account', 'transaction_date']),
            models.Index(fields=['category', 'transaction_date']),
        ]

    def __str__(self):
        return f'{self.description} - R$ {self.amount} ({self.get_transaction_type_display()})'
