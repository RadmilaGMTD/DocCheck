from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(email="raf1507@mail.ru", first_name="radmila", last_name="mila")
        user.set_password("radmila68")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully created admin user with email {user.email}"))
