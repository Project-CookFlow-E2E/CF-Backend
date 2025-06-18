from django.core.management.base import BaseCommand
from recipes.models.recipe import Recipe
from users.models.user import CustomUser
from recipes.models.category import Category
from recipes.models.step import Step


class Command(BaseCommand):
    help = "Seed initial recipes into the database."

    def handle(self, *args, **options):
        try:
            user = CustomUser.objects.get(username="cookflow")
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR("El usuario 'cookflow' no existe."))
            return

        seed_data = [
            {
                "name": "Tortilla de papas",
                "description": "La clásica tortilla española.",
                "user_id": user,
                "duration_minutes": 30,
                "commensals": 4,
                "categories": [5,7],
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
                "categories": [5,6],
                "steps": [
                    {
                        "order": 1,
                        "description": "Empaniza la milanesa con huevo y pan rallado.",
                    },
                    {
                        "order": 2,
                        "description": "Fríe la milanesa en aceite caliente.",
                    },
                    {
                        "order": 3,
                        "description": "Agrega salsa de tomate y queso por encima.",
                    },
                    {
                        "order": 4,
                        "description": "Gratina en el horno hasta que el queso se derrita.",
                    },
                ],
            },
            {
                "name": "Hamburguesa casera",
                "description": "Una jugosa hamburguesa con todos los ingredientes.",
                "user_id": user,
                "duration_minutes": 30,
                "commensals": 4,
                "categories": [5, 7],
                "steps": [
                    {
                        "order": 1,
                        "description": "Forma las hamburguesas con la carne molida.",
                    },
                    {
                        "order": 2,
                        "description": "Fríelas en aceite hasta que estén doradas.",
                    },
                    {
                        "order": 3,
                        "description": "Coloca las hamburguesas en pan con los ingredientes deseados.",
                    },
                ],
            },
        ]

        for data in seed_data:
            recipe, created = Recipe.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "user_id": user,
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
