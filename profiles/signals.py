"""
Signals for the profiles app.

Automatically creates a Profile instance when a new User is created.
"""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

# TODO: Implement default categories creation after categories.utils module is ready
# from categories.utils import create_default_categories_for_user


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile automatically when a new User is created.

    Args:
        sender: The model class (User)
        instance: The actual User instance being saved
        created: Boolean indicating if this is a new User
        **kwargs: Additional keyword arguments
    """
    if created:
        Profile.objects.create(
            user=instance,
            first_name='',
            last_name=''
        )


# TODO: Uncomment this signal when categories.utils.create_default_categories_for_user is implemented
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_default_categories(sender, instance, created, **kwargs):
#     """
#     Create default categories automatically when a new User is created.
#
#     Args:
#         sender: The model class (User)
#         instance: The actual User instance being saved
#         created: Boolean indicating if this is a new User
#         **kwargs: Additional keyword arguments
#     """
#     if created:
#         create_default_categories_for_user(instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the Profile whenever the User is saved.

    This ensures the profile is kept in sync with user updates.

    Args:
        sender: The model class (User)
        instance: The actual User instance being saved
        **kwargs: Additional keyword arguments
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
