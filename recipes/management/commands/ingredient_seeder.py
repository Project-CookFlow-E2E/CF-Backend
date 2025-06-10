from django.core.management.base import BaseCommand
from recipes.models.ingredient import Ingredient
from users.models.user import CustomUser
from recipes.models.category import Category
from measurements.models.unitType import UnitType

class Command(BaseCommand):
    help = "Seed initial ingredients into the database."

    def handle(self, *args, **kwargs):
        # Crear usuario admin si no existe
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
                "password": "admin12345",
            },
        )
        if not user.check_password("admin12345"):
            user.set_password("admin12345")
            user.save()

        # Crear categoría general si no existe
        category, _ = Category.objects.get_or_create(name="General")

        # Obtener UnitType, por ejemplo "Cantidad"
        unit_type = UnitType.objects.get(name="Cantidad")

        ingredients_data = [
            {"name": "Papa"},
            {"name": "Huevo"},
            {"name": "Leche"},
            {"name": "Aceite"},
            {"name": "Sal"},
        ]

        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_data["name"],
                defaults={
                    "user_id": user,
                    "unit_type_id": unit_type,
                    "is_approved": True,
                },
            )
            # Añadir categoría
            ingredient.categories.add(category)
            ingredient.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created ingredient: {ingredient.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Ingredient already exists: {ingredient.name}"))
