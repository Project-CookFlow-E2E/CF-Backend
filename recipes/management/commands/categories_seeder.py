from django.core.management.base import BaseCommand
from recipes.models.category import Category
from users.models.user import CustomUser  # Ajusta si tu modelo user está aquí

class Command(BaseCommand):
    help = "Seed initial categories into the database."

    def handle(self, *args, **options):
        # Obtiene el usuario por defecto (id=1) o crea uno si no existe
        user, _ = CustomUser.objects.get_or_create(
            id=1,
            defaults={
                "username": "admin",
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

        # Lista de categorías iniciales (sin parent_category_id, ejemplo)
        categories_data = [
            {"name": "Categorias", "parent_category_id_id":0, "user_id": user},
            {"name": "Tipo de cocina", "parent_category_id_id":0, "user_id": user},
            {"name": "Origen", "parent_category_id_id":0, "user_id": user},
            {"name": "Comida", "parent_category_id_id":1, "user_id": user},
            {"name": "Desayuno", "parent_category_id_id":1, "user_id": user},
            {"name": "Brunch", "parent_category_id_id":1, "user_id": user},
            {"name": "Cena", "parent_category_id_id":1, "user_id": user},
            {"name": "Postre", "parent_category_id_id":1, "user_id": user},
            {"name": "Merienda", "parent_category_id_id":1, "user_id": user},
            {"name": "Snack", "parent_category_id_id":1, "user_id": user},
            {"name": "Cocido", "parent_category_id_id":2, "user_id": user},
            {"name": "Al vapor", "parent_category_id_id":2, "user_id": user},
            {"name": "Hervido", "parent_category_id_id":2, "user_id": user},
            {"name": "Guiso", "parent_category_id_id":2,"user_id": user},
            {"name": "Frito", "parent_category_id_id":2, "user_id": user},
            {"name": "A la plancha", "parent_category_id_id":2, "user_id": user},
            {"name": "Asado", "parent_category_id_id":2, "user_id": user},
            {"name": "Sopas", "parent_category_id_id":2, "user_id": user},
            {"name": "Italiana", "parent_category_id_id":3, "user_id": user},
            {"name": "Griega", "parent_category_id_id":3, "user_id": user},
            {"name": "Española", "parent_category_id_id":3, "user_id": user},
            {"name": "Japonesa", "parent_category_id_id":3, "user_id": user},
            {"name": "Americana", "parent_category_id_id":3, "user_id": user}
        ]


        # Crea o actualiza las categorías
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={
                    "user_id": cat_data["user_id"],
                    "parent_category_id": None,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {category.name}"))
