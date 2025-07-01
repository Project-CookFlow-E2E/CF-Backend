# cf-backend/recipes/management/commands/ingredient_seeder.py
from django.core.management.base import BaseCommand
from recipes.models.ingredient import Ingredient
from users.models.user import CustomUser
from recipes.models.category import Category
from measurements.models.unitType import UnitType

class Command(BaseCommand):
    help = "Seed initial ingredients into the database."

    def handle(self, *args, **kwargs):
        self.stdout.write("Ejecutando ingredient_seeder...")

        # Obtener usuario admin (asumiendo que users_seeder ya lo creó con id=1)
        try:
            user = CustomUser.objects.get(id=1)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR("Error: Admin user (ID=1) not found. Run users_seeder first!"))
            return

        # Get the "General" category, assuming categories_seeder has created it
        try:
            category = Category.objects.get(name="General")
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("Error: Category 'General' not found. Run categories_seeder first!"))
            return

        # Obtener UnitType "unitario" (asumiendo que unitType_seeder ya lo creó)
        try:
            unit_type = UnitType.objects.get(name="unitario")
        except UnitType.DoesNotExist:
            self.stdout.write(self.style.ERROR("Error: UnitType 'unitario' not found. Run unitType_seeder first!"))
            return

        ingredients_data = [
            {"name": "Papa"},
            {"name": "Huevo"},
            {"name": "Leche"},
            {"name": "Aceite"},
            {"name": "Sal"},
            {"name": "Cebolla"}
        ]

        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_data["name"],
                defaults={
                    "user_id": user, # Assign the fetched admin user
                    "unit_type_id": unit_type,
                    "is_approved": True,
                },
            )
            # Add category to the ingredient (for both new and existing)
            ingredient.categories.add(category)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created ingredient: {ingredient.name}"))
            else:
                # If ingredient already exists, update its user_id and unit_type if necessary
                needs_update = False
                if ingredient.user_id != user:
                    ingredient.user_id = user
                    needs_update = True
                if ingredient.unit_type_id != unit_type:
                    ingredient.unit_type_id = unit_type
                    needs_update = True

                if needs_update:
                    ingredient.save() # Save only if updates were made
                    self.stdout.write(self.style.WARNING(f"Updated existing ingredient: {ingredient.name} user/type."))
                else:
                    self.stdout.write(self.style.WARNING(f"Ingredient already exists: {ingredient.name}"))
        self.stdout.write("✅ ingredient_seeder completado.")
