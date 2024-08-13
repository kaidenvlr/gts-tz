from django.conf import settings
from apps.users.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Create Superuser CLI Command
    """
    help = "Create user if it does not exist"

    def handle(self, *args, **options):
        """
        Handler to catch this CLI command
        """
        if not User.objects.filter(username=settings.USER_USERNAME):
            User.objects.create_user(
                username=settings.USER_USERNAME,
                email=settings.USER_EMAIL,
                password=settings.USER_PASSWORD
            )
            self.stdout.write("Successfully created.")
        else:
            self.stdout.write("User already exist.")