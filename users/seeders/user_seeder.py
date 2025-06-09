from django.core.management.base import BaseCommand
from users.models.user import CustomUser

class Command(BaseCommand):
    help = 'Seed initial users into the database.'

    def handle(self, *args, **options):
        seed_data = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'name': 'Admin',
                'surname': 'Principal',
                'second_surname': 'Root',
                'biography': 'Super user of the system',
                'is_staff': True,
                'is_superuser': True,
                'password': 'admin12345'
            },
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'name': 'User',
                'surname': 'Uno',
                'second_surname': 'Test',
                'biography': 'Primer usuario de prueba',
                'is_staff': False,
                'is_superuser': False,
                'password': 'user12345'
            },
            # Add more users as needed
        ]

        for data in seed_data:
            if not CustomUser.objects.filter(username=data['username']).exists():
                user = CustomUser.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    name=data['name'],
                    surname=data['surname'],
                    second_surname=data['second_surname'],
                    biography=data['biography'],
                    is_staff=data['is_staff'],
                    is_superuser=data['is_superuser'],
                )
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"User already exists: {data['username']}"))

