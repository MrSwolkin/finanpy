from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from categories.utils import create_default_categories_for_user


User = get_user_model()


class Command(BaseCommand):
    help = 'Creates default income and expense categories for users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user_id',
            type=int,
            help='Create categories for a specific user ID. If not provided, creates for all users without default categories.'
        )

    def handle(self, *args, **options):
        user_id = options.get('user_id')

        # Get users to process
        if user_id:
            try:
                users = [User.objects.get(pk=user_id)]
                self.stdout.write(f'Processing user ID: {user_id}')
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with ID {user_id} does not exist')
                )
                return
        else:
            users = User.objects.all()
            self.stdout.write(f'Processing all users ({users.count()} total)')

        total_created = 0
        total_existing = 0

        for user in users:
            self.stdout.write(f'\nProcessing user: {user.email}')

            created_count, existing_count = create_default_categories_for_user(user)

            total_created += created_count
            total_existing += existing_count

            if created_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Created {created_count} new categories'
                    )
                )
            if existing_count > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'  {existing_count} categories already existed'
                    )
                )

            self.stdout.write(
                f'  Summary for {user.email}: {created_count} created, {existing_count} already existed'
            )

        # Final summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(
            self.style.SUCCESS(
                f'TOTAL: {total_created} categories created, {total_existing} already existed'
            )
        )
