from django.core.management.base import BaseCommand
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.recipe import Recipe
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit


class Command(BaseCommand):
    help = 'Seed RecipeIngredient table with dummy data'

    def handle(self, *args, **kwargs):
        try:
            recipes = list(Recipe.objects.all())
            ingredients = list(Ingredient.objects.all())
            unit = Unit.objects.first()

            if len(recipes) < 2 or len(ingredients) < 6 or not unit:
                self.stdout.write(self.style.ERROR("Se requieren al menos 2 recetas, 6 ingredientes y una unidad."))
                return

            data = [
                {'recipe': recipes[0], 'ingredient': ingredients[1], 'quantity': 3, 'unit': unit},
                {'recipe': recipes[0], 'ingredient': ingredients[0], 'quantity': 2, 'unit': unit},
                {'recipe': recipes[0], 'ingredient': ingredients[3], 'quantity': 1, 'unit': unit},
                {'recipe': recipes[0], 'ingredient': ingredients[4], 'quantity': 1, 'unit': unit},
                {'recipe': recipes[0], 'ingredient': ingredients[5], 'quantity': 1, 'unit': unit},
                {'recipe': recipes[1], 'ingredient': ingredients[2], 'quantity': 1, 'unit': unit},
                {'recipe': recipes[1], 'ingredient': ingredients[4], 'quantity': 1, 'unit': unit},
                {'recipe': recipes[1], 'ingredient': ingredients[1], 'quantity': 1, 'unit': unit},
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
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
