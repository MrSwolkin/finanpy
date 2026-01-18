from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Model representing a financial transaction category.
    Can be either income or expense type.
    """
    INCOME = 'income'
    EXPENSE = 'expense'

    CATEGORY_TYPE_CHOICES = [
        (INCOME, 'Receita'),
        (EXPENSE, 'Despesa'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Usuário'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )
    category_type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPE_CHOICES,
        verbose_name='Tipo'
    )
    color = models.CharField(
        max_length=7,
        default='#6b7280',
        verbose_name='Cor',
        help_text='Cor em formato hexadecimal (ex: #6b7280)'
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='Categoria padrão',
        help_text='Categorias padrão não podem ser excluídas'
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
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ['user', 'name']
        indexes = [
            models.Index(fields=['user', 'category_type']),
        ]

    def __str__(self):
        return f'{self.name} ({self.get_category_type_display()})'
