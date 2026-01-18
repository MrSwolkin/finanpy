from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user manager that uses email as the unique identifier
    instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.

        Args:
            email: User's email address (required)
            password: User's password
            **extra_fields: Additional fields for the user model

        Returns:
            CustomUser instance

        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.

        Args:
            email: User's email address (required)
            password: User's password
            **extra_fields: Additional fields for the user model

        Returns:
            CustomUser instance with superuser privileges
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that uses email as the unique identifier
    instead of username for authentication.
    """

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail',
        help_text='Endereço de e-mail do usuário'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email
