from django.core.management.base import BaseCommand
from recipes.models.recipe import Recipe
from users.models.user import CustomUser
from recipes.models.category import Category
from recipes.models.step import Step


class Command(BaseCommand):
    help = "Seed initial recipes into the database."

    def handle(self, *args, **options):
        # Busca usuario y categoría de ejemplo, crea si no existen
        user, _ = CustomUser.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "name": "Admin",
                "surname": "Principal",
                "second_surname": "Root",
                "biography": "Super user of the system",
                "is_staff": True,
                "is_superuser": True,
                "password": "admin12345",  # Ojo, esto no la hashea, solo para seeds iniciales
            },
        )
        # Si el user fue recién creado, setea la password de forma segura
        if not user.check_password("admin12345"):
            user.set_password("admin12345")
            user.save()

        category, _ = Category.objects.get_or_create(name="General", defaults={})

        seed_data = [
            {
                "name": "Tortilla de papas",
                "description": "La clásica tortilla española.",
                "user_id": user,
                "duration_minutes": 30,
                "commensals": 4,
                "categories": [category],
                "steps": [
                    {
                        "order": 1,
                        "description": "Pela y corta las papas en rodajas finas.",
                    },
                    {
                        "order": 2,
                        "description": "Fríelas en aceite hasta que estén blandas.",
                    },
                    {
                        "order": 3,
                        "description": "Bate los huevos y mezcla con las papas.",
                    },
                    {
                        "order": 4,
                        "description": "Cuaja la mezcla en una sartén por ambos lados.",
                    },
                ],
            },
            {
                "name": "Milanesa a la napolitana",
                "description": "Milanesa con salsa y queso.",
                "user_id": user,
                "duration_minutes": 45,
                "commensals": 2,
                "categories": [category],
            },
        ]

        for data in seed_data:
            recipe, created = Recipe.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "user_id": data["user_id"],
                    "duration_minutes": data["duration_minutes"],
                    "commensals": data["commensals"],
                },
            )
            if created:
                recipe.categories.set(data["categories"])
                steps = data.get("steps", [])
                for step in steps:
                    Step.objects.create(
                        order=step["order"],
                        description=step["description"],
                        recipe_id=recipe
                    )
                self.stdout.write(self.style.SUCCESS(f"Created recipe: {recipe.name}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Recipe already exists: {recipe.name}")
                )
