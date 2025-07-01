# CF-backend/recipes/management/commands/recipe_seeder.py
from django.core.management.base import BaseCommand
from recipes.models.recipe import Recipe
from users.models.user import CustomUser
from recipes.models.category import Category # Imported but not directly used in the loop, kept for completeness
from recipes.models.step import Step


class Command(BaseCommand):
    help = "Seed initial recipes into the database."

    def handle(self, *args, **options):
        self.stdout.write("Ejecutando recipe_seeder...")
        try:
            # Fetch the 'cookflow' user, assuming users_seeder has created it
            user = CustomUser.objects.get(username="cookflow")
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR("El usuario 'cookflow' no existe. Asegúrate de que 'users_seeder' se haya ejecutado correctamente."))
            return

        seed_data = [
            {
                "name": "Tortilla de papas",
                "description": "La clásica tortilla española.",
                "user_id": user, # Assign the fetched 'cookflow' user
                "duration_minutes": 30,
                "commensals": 4,
                "categories": [5,7], # These are category IDs
                "steps": [
                    {"order": 1, "description": "Pela y corta las papas en rodajas finas."},
                    {"order": 2, "description": "Fríelas en aceite hasta que estén blandas."},
                    {"order": 3, "description": "Bate los huevos y mezcla con las papas."},
                    {"order": 4, "description": "Cuaja la mezcla en una sartén por ambos lados."},
                ],
            },
            {
                "name": "Milanesa a la napolitana",
                "description": "Milanesa con salsa y queso.",
                "user_id": user, # Assign the fetched 'cookflow' user
                "duration_minutes": 45,
                "commensals": 2,
                "categories": [5,6], # These are category IDs
                "steps": [
                    {"order": 1, "description": "Empaniza la milanesa con huevo y pan rallado."},
                    {"order": 2, "description": "Fríe la milanesa en aceite caliente."},
                    {"order": 3, "description": "Agrega salsa de tomate y queso por encima."},
                    {"order": 4, "description": "Gratina en el horno hasta que el queso se derrita."},
                ],
            },
            {
                "name": "Hamburguesa casera",
                "description": "Una jugosa hamburguesa con todos los ingredientes.",
                "user_id": user, # Assign the fetched 'cookflow' user
                "duration_minutes": 30,
                "commensals": 4,
                "categories": [5, 7], # These are category IDs
                "steps": [
                    {"order": 1, "description": "Forma las hamburguesas con la carne molida."},
                    {"order": 2, "description": "Fríelas en aceite hasta que estén doradas."},
                    {"order": 3, "description": "Coloca las hamburguesas en pan con los ingredientes deseados."},
                ],
            },
        ]

        for data in seed_data:
            recipe, created = Recipe.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "user_id": user, # Ensure user_id is passed here
                    "duration_minutes": data["duration_minutes"],
                    "commensals": data["commensals"],
                },
            )
            if created:
                # Set categories for new recipes
                # Fetch Category objects from IDs
                category_objects = Category.objects.filter(id__in=data["categories"])
                recipe.categories.set(category_objects)
                
                # Create steps for new recipes
                steps = data.get("steps", [])
                for step in steps:
                    Step.objects.create(
                        order=step["order"],
                        description=step["description"],
                        recipe=recipe # <--- CORRECTED THIS LINE: Assign the Recipe object directly
                    )
                self.stdout.write(self.style.SUCCESS(f"Created recipe: {recipe.name}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Recipe already exists: {recipe.name}")
                )
        self.stdout.write("✅ recipe_seeder completado.")
