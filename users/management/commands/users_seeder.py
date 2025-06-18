from django.core.management.base import BaseCommand
from users.models import CustomUser  # Asegúrate de que la ruta sea correcta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed the database with initial users'

    def handle(self, *args, **kwargs):
        users_data = [
            {
                'username': 'juan123',
                'email': 'juan@example.com',
                'name': 'Juan',
                'surname': 'Pérez',
                'second_surname': 'García',
                'biography': 'Amante de la cocina tradicional.',
                'password': 'testpass123',
            },
            {
                'username': 'ana456',
                'email': 'ana@example.com',
                'name': 'Ana',
                'surname': 'López',
                'second_surname': 'Martínez',
                'biography': 'Chef profesional.',
                'password': 'testpass456',
            },
            {
                'username': 'mario789',
                'email': 'mario@example.com',
                'name': 'Mario',
                'surname': 'Sánchez',
                'second_surname': 'Ruiz',
                'biography': 'Explorador de sabores.',
                'password': 'testpass789',
            },
        ]

        for user_data in users_data:
            if not CustomUser.objects.filter(username=user_data['username']).exists():
                is_superuser = user_data.pop('is_superuser', False)
                is_staff = user_data.pop('is_staff', False)
                password = user_data.pop('password')

                user = CustomUser.objects.create_user(**user_data)
                user.set_password(password)
                user.is_superuser = is_superuser
                user.is_staff = is_staff
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario "{user.username}" creado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Usuario "{user_data["username"]}" ya existe.'))
