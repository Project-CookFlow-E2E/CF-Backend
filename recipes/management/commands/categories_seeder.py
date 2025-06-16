from django.core.management.base import BaseCommand
from recipes.models.category import Category
from users.models.user import CustomUser

class Command(BaseCommand):
    help = "Seed initial categories into the database."

    def handle(self, *args, **options):
        # Crear usuario admin
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
                "is_superuser": True}
        )
        if not user.check_password("admin12345"):
            user.set_password("admin12345")
            user.save()

        # Lista de categorías con claves numéricas para poder relacionarlas
        categories_data = [
            {"id": 1, "name": "Root", "parent_category_id": None, "user_id":1},
            {"id": 2, "name": "Categorias", "parent_category_id": 1, "user_id":1},
            {"id": 3, "name": "Tipo de cocina", "parent_category_id": 1, "user_id":1},
            {"id": 4, "name": "Origen", "parent_category_id": 1, "user_id":1},
            {"id": 5, "name": "Comida", "parent_category_id": 2, "user_id":1},
            {"id": 6, "name": "Desayuno", "parent_category_id": 2, "user_id":1},
            {"id": 7, "name": "Brunch", "parent_category_id": 2, "user_id":1},
            {"id": 8, "name": "Cena", "parent_category_id": 2, "user_id":1},
            {"id": 9, "name": "Postre", "parent_category_id": 2, "user_id":1},
            {"id": 10, "name": "Merienda", "parent_category_id": 2, "user_id":1},
            {"id": 11, "name": "Snack", "parent_category_id": 2, "user_id":1},
            {"id": 12, "name": "Cocido", "parent_category_id": 3, "user_id":1},
            {"id": 13, "name": "Al vapor", "parent_category_id": 3, "user_id":1},
            {"id": 14, "name": "Hervido", "parent_category_id": 3, "user_id":1},
            {"id": 15, "name": "Guiso", "parent_category_id": 3, "user_id":1},
            {"id": 16, "name": "Frito", "parent_category_id": 3, "user_id":1},
            {"id": 17, "name": "A la plancha", "parent_category_id": 3, "user_id":1},
            {"id": 18, "name": "Asado", "parent_category_id": 3, "user_id":1},
            {"id": 19, "name": "Sopas", "parent_category_id": 3, "user_id":1},
            {"id": 20, "name": "Italiana", "parent_category_id": 4, "user_id":1},
            {"id": 21, "name": "Griega", "parent_category_id": 4, "user_id":1},
            {"id": 22, "name": "Española", "parent_category_id": 4, "user_id":1},
            {"id": 22, "name": "Japonesa", "parent_category_id": 4, "user_id":1},
            {"id": 23, "name": "Americana", "parent_category_id": 4, "user_id":1}
        ]

        # Diccionario para guardar las instancias creadas por ID
        created_categories = {}

        # Paso 1: crear todas sin padre
        for cat in categories_data:
            if cat["parent_category_id"] is None:
                category, _ = Category.objects.get_or_create(
                    name=cat["name"]
                )
                created_categories[cat["id"]] = category
                self.stdout.write(self.style.SUCCESS(f"Created root category: {category.name}"))

        # Paso 2: crear con padre ya creado
        for cat in categories_data:
            if cat["parent_category_id"] is not None:
                parent = created_categories.get(cat["parent_category_id"])
                category, created = Category.objects.get_or_create(
                    name=cat["name"],
                    user_id=user,
                    parent_category_id=parent
            
                )
                created_categories[cat["id"]] = category
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created category: {category.name} (child of {parent.name})"))
                else:
                    self.stdout.write(self.style.WARNING(f"Category already exists: {category.name}"))

