from django.conf import settings
from django.db import models


class Account(models.Model):
    """
    Bank account model for managing user financial accounts.
    Supports different account types (checking, savings, investment, other).
    """

    # Account type choices
    CHECKING = 'checking'
    SAVINGS = 'savings'
    INVESTMENT = 'investment'
    OTHER = 'other'

    ACCOUNT_TYPE_CHOICES = [
        (CHECKING, 'Conta Corrente'),
        (SAVINGS, 'Poupança'),
        (INVESTMENT, 'Investimento'),
        (OTHER, 'Outro'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='Usuário'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default=CHECKING,
        verbose_name='Tipo de Conta'
    )
    initial_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Saldo Inicial'
    )
    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Saldo Atual'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
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
        ordering = ['name']
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['user', 'account_type']),
        ]

    def __str__(self):
        return self.name
