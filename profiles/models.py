from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    User profile model containing personal information.
    Each user has one profile with extended data like name, phone, and avatar.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuário'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Nome',
        help_text='Primeiro nome do usuário'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Sobrenome',
        help_text='Sobrenome do usuário'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone',
        help_text='Número de telefone com DDD'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar',
        help_text='Foto de perfil do usuário'
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
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['user']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self) -> str:
        """Return full name of the user."""
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self) -> str:
        """Return full name as a property."""
        return f'{self.first_name} {self.last_name}'
