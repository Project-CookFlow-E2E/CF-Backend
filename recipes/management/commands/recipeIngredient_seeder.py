# cf-backend/recipes/management/commands/recipeIngredient_seeder.py
from django.core.management.base import BaseCommand
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.recipe import Recipe
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit


class Command(BaseCommand):
    help = 'Seed RecipeIngredient table with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Ejecutando recipeIngredient_seeder...")
        try:
            recipes = list(Recipe.objects.all())
            ingredients = list(Ingredient.objects.all())
            unit = Unit.objects.first() # Get the first available unit

            if len(recipes) < 2 or len(ingredients) < 6 or not unit:
                self.stdout.write(self.style.ERROR("Se requieren al menos 2 recetas, 6 ingredientes y una unidad. Asegúrate de que los seeders de recetas, ingredientes y unidades se hayan ejecutado correctamente."))
                return

            data = [
                {'recipe': recipes[0], 'ingredient': ingredients[1], 'quantity': 3, 'unit': unit}, # Tortilla de papas: Huevo
                {'recipe': recipes[0], 'ingredient': ingredients[0], 'quantity': 2, 'unit': unit}, # Tortilla de papas: Papa
                {'recipe': recipes[0], 'ingredient': ingredients[3], 'quantity': 1, 'unit': unit}, # Tortilla de papas: Aceite
                {'recipe': recipes[0], 'ingredient': ingredients[4], 'quantity': 1, 'unit': unit}, # Tortilla de papas: Sal
                {'recipe': recipes[0], 'ingredient': ingredients[5], 'quantity': 1, 'unit': unit}, # Tortilla de papas: Cebolla (if used)
                
                # Assuming recipes[1] is Milanesa a la napolitana
                # You'll need to ensure ingredients match the recipe.
                # Example for Milanesa:
                # {'recipe': recipes[1], 'ingredient': ingredients[...], 'quantity': ..., 'unit': unit}, # Milanesa (e.g., meat)
                # {'recipe': recipes[1], 'ingredient': ingredients[...], 'quantity': ..., 'unit': unit}, # Salsa de tomate
                # {'recipe': recipes[1], 'ingredient': ingredients[...], 'quantity': ..., 'unit': unit}, # Queso
                
                # For demonstration, using existing ingredients for Milanesa
                {'recipe': recipes[1], 'ingredient': ingredients[2], 'quantity': 1, 'unit': unit}, # Milanesa: Leche (example)
                {'recipe': recipes[1], 'ingredient': ingredients[4], 'quantity': 1, 'unit': unit}, # Milanesa: Sal
                {'recipe': recipes[1], 'ingredient': ingredients[1], 'quantity': 1, 'unit': unit}, # Milanesa: Huevo (for breading)
                
                # Assuming recipes[2] is Hamburguesa casera
                # {'recipe': recipes[2], 'ingredient': ingredients[...], 'quantity': ..., 'unit': unit}, # Carne molida
                # {'recipe': recipes[2], 'ingredient': ingredients[...], 'quantity': ..., 'unit': unit}, # Pan de hamburguesa
            ]

            for entry in data:
                obj, created = RecipeIngredient.objects.get_or_create(
                    recipe=entry['recipe'],
                    ingredient=entry['ingredient'],
                    defaults={
                        'quantity': entry['quantity'],
                        'unit': entry['unit']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Agregado: {entry['ingredient'].name} a {entry['recipe'].name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Ya existe: {entry['ingredient'].name} en {entry['recipe'].name}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error en recipeIngredient_seeder: {str(e)}"))
        self.stdout.write("✅ recipeIngredient_seeder completado.")


# from django.core.management.base import BaseCommand
# from recipes.models.recipeIngredient import RecipeIngredient
# from recipes.models.recipe import Recipe
# from recipes.models.ingredient import Ingredient
# from measurements.models.unit import Unit


# class Command(BaseCommand):
#     help = 'Seed RecipeIngredient table with dummy data'

#     def handle(self, *args, **kwargs):
#         try:
#             recipes = list(Recipe.objects.all())
#             ingredients = list(Ingredient.objects.all())
#             unit = Unit.objects.first()

#             if len(recipes) < 2 or len(ingredients) < 6 or not unit:
#                 self.stdout.write(self.style.ERROR("Se requieren al menos 2 recetas, 6 ingredientes y una unidad."))
#                 return

#             data = [
#                 {'recipe': recipes[0], 'ingredient': ingredients[1], 'quantity': 3, 'unit': unit},
#                 {'recipe': recipes[0], 'ingredient': ingredients[0], 'quantity': 2, 'unit': unit},
#                 {'recipe': recipes[0], 'ingredient': ingredients[3], 'quantity': 1, 'unit': unit},
#                 {'recipe': recipes[0], 'ingredient': ingredients[4], 'quantity': 1, 'unit': unit},
#                 {'recipe': recipes[0], 'ingredient': ingredients[5], 'quantity': 1, 'unit': unit},
#                 {'recipe': recipes[1], 'ingredient': ingredients[2], 'quantity': 1, 'unit': unit},
#                 {'recipe': recipes[1], 'ingredient': ingredients[4], 'quantity': 1, 'unit': unit},
#                 {'recipe': recipes[1], 'ingredient': ingredients[1], 'quantity': 1, 'unit': unit},
#             ]

#             for entry in data:
#                 obj, created = RecipeIngredient.objects.get_or_create(
#                     recipe=entry['recipe'],
#                     ingredient=entry['ingredient'],
#                     defaults={
#                         'quantity': entry['quantity'],
#                         'unit': entry['unit']
#                     }
#                 )
#                 if created:
#                     self.stdout.write(self.style.SUCCESS(f"Agregado: {entry['ingredient'].name} a {entry['recipe'].name}"))
#                 else:
#                     self.stdout.write(self.style.WARNING(f"Ya existe: {entry['ingredient'].name} en {entry['recipe'].name}"))

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
