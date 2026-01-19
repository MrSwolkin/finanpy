"""
Signals for the transactions app.

Automatically updates Account balance when transactions are created, updated, or deleted.
"""

from decimal import Decimal
from django.db import transaction
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Transaction


@receiver(pre_save, sender=Transaction)
def revert_old_transaction_balance(sender, instance, **kwargs):
    """
    Revert the balance impact of the old transaction before saving changes.

    This runs before saving an edited transaction to remove the old value's
    impact from the account balance. The new value will be applied by post_save.

    Args:
        sender: The model class (Transaction)
        instance: The Transaction instance being saved
        **kwargs: Additional keyword arguments
    """
    # Only process if this is an update (instance already exists in database)
    if instance.pk:
        try:
            # Get the old transaction data from database
            old_transaction = Transaction.objects.get(pk=instance.pk)
            old_account = old_transaction.account
            old_amount = old_transaction.amount
            old_type = old_transaction.transaction_type

            # Revert the old transaction's impact on the old account
            with transaction.atomic():
                # Lock the account row for update to prevent race conditions
                old_account = old_account.__class__.objects.select_for_update().get(pk=old_account.pk)

                if old_type == Transaction.INCOME:
                    # If it was income, subtract it from balance
                    old_account.current_balance -= old_amount
                else:  # EXPENSE
                    # If it was expense, add it back to balance
                    old_account.current_balance += old_amount

                old_account.save(update_fields=['current_balance', 'updated_at'])

        except Transaction.DoesNotExist:
            # This shouldn't happen, but handle gracefully
            pass


@receiver(post_save, sender=Transaction)
def update_account_balance_on_save(sender, instance, created, **kwargs):
    """
    Update account balance when a transaction is created or updated.

    For income transactions: increases the account balance
    For expense transactions: decreases the account balance

    Args:
        sender: The model class (Transaction)
        instance: The Transaction instance being saved
        created: Boolean indicating if this is a new Transaction
        **kwargs: Additional keyword arguments
    """
    # Use atomic transaction to ensure data integrity
    with transaction.atomic():
        # Lock the account row for update to prevent race conditions
        account = instance.account.__class__.objects.select_for_update().get(pk=instance.account.pk)

        # Calculate impact on balance based on transaction type
        if instance.transaction_type == Transaction.INCOME:
            # Income increases the balance
            account.current_balance += instance.amount
        else:  # EXPENSE
            # Expense decreases the balance
            account.current_balance -= instance.amount

        # Save the updated balance
        account.save(update_fields=['current_balance', 'updated_at'])


@receiver(post_delete, sender=Transaction)
def revert_account_balance_on_delete(sender, instance, **kwargs):
    """
    Revert account balance when a transaction is deleted.

    Removes the transaction's impact from the account balance:
    - For income: decreases the account balance
    - For expense: increases the account balance (reverting the deduction)

    Args:
        sender: The model class (Transaction)
        instance: The Transaction instance being deleted
        **kwargs: Additional keyword arguments
    """
    # Use atomic transaction to ensure data integrity
    with transaction.atomic():
        # Lock the account row for update to prevent race conditions
        account = instance.account.__class__.objects.select_for_update().get(pk=instance.account.pk)

        # Revert the transaction's impact on balance
        if instance.transaction_type == Transaction.INCOME:
            # If it was income, subtract it from balance
            account.current_balance -= instance.amount
        else:  # EXPENSE
            # If it was expense, add it back to balance
            account.current_balance += instance.amount

        # Save the updated balance
        account.save(update_fields=['current_balance', 'updated_at'])
