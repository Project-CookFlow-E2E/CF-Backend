# CF-backend/users/management/commands/users_seeder.py
from django.core.management.base import BaseCommand
from users.models.user import CustomUser
from django.contrib.auth.hashers import make_password
from django.db import connection

class Command(BaseCommand):
    help = 'Seeds initial user data.'

    def handle(self, *args, **options):
        self.stdout.write("Ejecutando users_seeder...")

        try:
            admin_user, created = CustomUser.objects.get_or_create(
                id=1,
                defaults={
                    'username': 'admin',
                    'email': 'admin@example.com',
                    'name': 'Admin',
                    'surname': 'Principal',
                    'biography': 'Super user of the system',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            if not admin_user.check_password("admin12345"):
                admin_user.set_password("admin12345")
                admin_user.save()
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Usuario "{admin_user.username}" (ID: {admin_user.id}) creado.'))
            else:
                needs_update = False
                if not admin_user.is_staff or not admin_user.is_superuser:
                    admin_user.is_staff = True
                    admin_user.is_superuser = True
                    needs_update = True
                if needs_update:
                    admin_user.save()
                    self.stdout.write(self.style.WARNING(f'Usuario "{admin_user.username}" (ID: {admin_user.id}) ya existe y fue actualizado.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Usuario "{admin_user.username}" (ID: {admin_user.id}) ya existe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error creating/getting admin user: {e}"))

        try:
            cookflow_user, created = CustomUser.objects.get_or_create(
                id=2,
                username='cookflow',
                defaults={
                    'email': 'cookflow@example.com',
                    'name': 'Cook',
                    'surname': 'Flow',
                    'password': make_password('cookflowpass'),
                    'is_staff': False,
                    'is_superuser': False,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Usuario "{cookflow_user.username}" creado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Usuario "{cookflow_user.username}" ya existe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error creating/getting cookflow user: {e}"))

        max_id = CustomUser.objects.all().order_by('-id').first().id if CustomUser.objects.exists() else 0
        
        sequence_name = f"{CustomUser._meta.db_table}_id_seq"

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT setval('{sequence_name}', {max_id + 1}, false);")
            self.stdout.write(self.style.NOTICE(f"Database sequence for {CustomUser._meta.db_table} reset to {max_id + 1}."))

        users_data = [
            {
                'username': 'juan123', 'email': 'juan@example.com', 'name': 'Juan',
                'surname': 'Pérez', 'second_surname': 'García',
                'biography': 'Amante de la cocina tradicional.', 'password': 'testpass123',
            },
            {
                'username': 'ana456', 'email': 'ana@example.com', 'name': 'Ana',
                'surname': 'López', 'second_surname': 'Martínez',
                'biography': 'Chef profesional.', 'password': 'testpass456',
            },
            {
                'username': 'mario789', 'email': 'mario@example.com', 'name': 'Mario',
                'surname': 'Sánchez', 'second_surname': 'Ruiz',
                'biography': 'Explorador de sabores.', 'password': 'testpass789',
            },
        ]

        for user_data in users_data:
            if not CustomUser.objects.filter(username=user_data['username']).exists():
                password = user_data.pop('password')

                user = CustomUser.objects.create_user(**user_data)
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario "{user.username}" creado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Usuario "{user_data["username"]}" ya existe.'))

        self.stdout.write("✅ users_seeder completado.")
