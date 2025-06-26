# from django.core.management.base import BaseCommand
# from recipes.models.category import Category
# from users.models.user import CustomUser

# class Command(BaseCommand):
#     help = "Seed initial categories into the database."

#     def handle(self, *args, **options):
#         # Crear usuario admin
#         user, _ = CustomUser.objects.get_or_create(
#             id=1,
#             defaults={
#                 "username": "admin",
#                 "email": "admin@example.com",
#                 "name": "Admin",
#                 "surname": "Principal",
#                 "second_surname": "Root",
#                 "biography": "Super user of the system",
#                 "is_staff": True,
#                 "is_superuser": True}
#         )
#         if not user.check_password("admin12345"):
#             user.set_password("admin12345")
#             user.save()

#         # Lista de categorías con claves numéricas para poder relacionarlas
#         categories_data = [
#             {"id": 1, "name": "Root", "parent_category_id": None, "user_id":1},
#             {"id": 2, "name": "Categorias", "parent_category_id": 1, "user_id":1},
#             {"id": 3, "name": "Tipo de cocina", "parent_category_id": 1, "user_id":1},
#             {"id": 4, "name": "Origen", "parent_category_id": 1, "user_id":1},
#             {"id": 5, "name": "Comida", "parent_category_id": 2, "user_id":1},
#             {"id": 6, "name": "Desayuno", "parent_category_id": 2, "user_id":1},
#             {"id": 7, "name": "Brunch", "parent_category_id": 2, "user_id":1},
#             {"id": 8, "name": "Cena", "parent_category_id": 2, "user_id":1},
#             {"id": 9, "name": "Postre", "parent_category_id": 2, "user_id":1},
#             {"id": 10, "name": "Merienda", "parent_category_id": 2, "user_id":1},
#             {"id": 11, "name": "Snack", "parent_category_id": 2, "user_id":1},
#             {"id": 12, "name": "Cocido", "parent_category_id": 3, "user_id":1},
#             {"id": 13, "name": "Al vapor", "parent_category_id": 3, "user_id":1},
#             {"id": 14, "name": "Hervido", "parent_category_id": 3, "user_id":1},
#             {"id": 15, "name": "Guiso", "parent_category_id": 3, "user_id":1},
#             {"id": 16, "name": "Frito", "parent_category_id": 3, "user_id":1},
#             {"id": 17, "name": "A la plancha", "parent_category_id": 3, "user_id":1},
#             {"id": 18, "name": "Asado", "parent_category_id": 3, "user_id":1},
#             {"id": 19, "name": "Sopas", "parent_category_id": 3, "user_id":1},
#             {"id": 20, "name": "Italiana", "parent_category_id": 4, "user_id":1},
#             {"id": 21, "name": "Griega", "parent_category_id": 4, "user_id":1},
#             {"id": 22, "name": "Española", "parent_category_id": 4, "user_id":1},
#             {"id": 22, "name": "Japonesa", "parent_category_id": 4, "user_id":1},
#             {"id": 23, "name": "Americana", "parent_category_id": 4, "user_id":1}
#         ]

#         # Diccionario para guardar las instancias creadas por ID
#         created_categories = {}

#         # Paso 1: crear todas sin padre
#         for cat in categories_data:
#             if cat["parent_category_id"] is None:
#                 category, _ = Category.objects.get_or_create(
#                     name=cat["name"]
#                 )
#                 created_categories[cat["id"]] = category
#                 self.stdout.write(self.style.SUCCESS(f"Created root category: {category.name}"))

#         # Paso 2: crear con padre ya creado
#         for cat in categories_data:
#             if cat["parent_category_id"] is not None:
#                 parent = created_categories.get(cat["parent_category_id"])
#                 category, created = Category.objects.get_or_create(
#                     name=cat["name"],
#                     user_id=user,
#                     parent_category_id=parent
            
#                 )
#                 created_categories[cat["id"]] = category
#                 if created:
#                     self.stdout.write(self.style.SUCCESS(f"Created category: {category.name} (child of {parent.name})"))
#                 else:
#                     self.stdout.write(self.style.WARNING(f"Category already exists: {category.name}"))

# cookflow-backend/recipes/management/commands/categories_seeder.py
from django.core.management.base import BaseCommand
from recipes.models.category import Category
from users.models.user import CustomUser # Assuming CustomUser is your user model

class Command(BaseCommand):
    help = "Seed initial categories into the database."

    def handle(self, *args, **options):
        self.stdout.write("Ejecutando categories_seeder...")

        # Ensure admin user exists (fetched, not created here)
        try:
            admin_user = CustomUser.objects.get(id=1)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR("Error: Admin user (ID=1) not found. Run users_seeder first!"))
            return

        # List of categories with numerical keys for relationships
        # FIXED: Changed ID for Japonesa from 22 to 24 to avoid duplicate primary key.
        # ADDED: "General" category with ID 25.
        categories_data = [
            {"id": 1, "name": "Root", "parent_category_id": None, "user_id": 1},
            {"id": 2, "name": "Categorias", "parent_category_id": 1, "user_id": 1},
            {"id": 3, "name": "Tipo de cocina", "parent_category_id": 1, "user_id": 1},
            {"id": 4, "name": "Origen", "parent_category_id": 1, "user_id": 1},
            {"id": 5, "name": "Comida", "parent_category_id": 2, "user_id": 1},
            {"id": 6, "name": "Desayuno", "parent_category_id": 2, "user_id": 1},
            {"id": 7, "name": "Brunch", "parent_category_id": 2, "user_id": 1},
            {"id": 8, "name": "Cena", "parent_category_id": 2, "user_id": 1},
            {"id": 9, "name": "Postre", "parent_category_id": 2, "user_id": 1},
            {"id": 10, "name": "Merienda", "parent_category_id": 2, "user_id": 1},
            {"id": 11, "name": "Snack", "parent_category_id": 2, "user_id": 1},
            {"id": 12, "name": "Cocido", "parent_category_id": 3, "user_id": 1},
            {"id": 13, "name": "Al vapor", "parent_category_id": 3, "user_id": 1},
            {"id": 14, "name": "Hervido", "parent_category_id": 3, "user_id": 1},
            {"id": 15, "name": "Guiso", "parent_category_id": 3, "user_id": 1},
            {"id": 16, "name": "Frito", "parent_category_id": 3, "user_id": 1},
            {"id": 17, "name": "A la plancha", "parent_category_id": 3, "user_id": 1},
            {"id": 18, "name": "Asado", "parent_category_id": 3, "user_id": 1},
            {"id": 19, "name": "Sopas", "parent_category_id": 3, "user_id": 1},
            {"id": 20, "name": "Italiana", "parent_category_id": 4, "user_id": 1},
            {"id": 21, "name": "Griega", "parent_category_id": 4, "user_id": 1},
            {"id": 22, "name": "Española", "parent_category_id": 4, "user_id": 1},
            {"id": 23, "name": "Americana", "parent_category_id": 4, "user_id": 1},
            {"id": 24, "name": "Japonesa", "parent_category_id": 4, "user_id": 1}, # Unique ID for Japonesa
            {"id": 25, "name": "General", "parent_category_id": 2, "user_id": 1} # NEW: General category under "Categorias"
        ]

        # Dictionary to store created category instances by their ID
        created_categories = {}

        # First pass: Create or get all categories without parents (Root and top-level children)
        # This ensures parents exist before children try to link to them
        for cat_data in categories_data:
            if cat_data["parent_category_id"] is None:
                category, created = Category.objects.get_or_create(
                    id=cat_data["id"], # Use ID for get_or_create
                    defaults={
                        "name": cat_data["name"],
                        "user_id": admin_user # Assign admin_user here
                    }
                )
                created_categories[cat_data["id"]] = category
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created root category: {category.name} (ID: {category.id})"))
                else:
                    # If category already exists, ensure its user is correct
                    if category.user_id != admin_user:
                        category.user_id = admin_user
                        category.save()
                        self.stdout.write(self.style.WARNING(f"Updated existing root category: {category.name} (ID: {category.id}) user."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Category already exists: {category.name} (ID: {category.id})"))
            else:
                # For categories with parents, ensure they are in the map for the second pass
                # This handles cases where a parent might be defined later in the list
                pass

        # Second pass: Create or get categories with parents, now that all potential parents exist
        for cat_data in categories_data:
            if cat_data["parent_category_id"] is not None:
                parent_category = created_categories.get(cat_data["parent_category_id"])
                if not parent_category:
                    self.stdout.write(self.style.ERROR(f"Parent category with ID {cat_data['parent_category_id']} not found for {cat_data['name']}. Skipping."))
                    continue # Skip if parent not found (shouldn't happen with correct order)

                category, created = Category.objects.get_or_create(
                    id=cat_data["id"], # Use ID for get_or_create
                    defaults={
                        "name": cat_data["name"],
                        "user_id": admin_user, # Assign admin_user here
                        "parent_category_id": parent_category,
                    }
                )
                # If the category already existed, ensure its parent and user are correctly set
                if not created:
                    needs_update = False
                    if category.parent_category_id != parent_category:
                        category.parent_category_id = parent_category
                        needs_update = True
                    if category.user_id != admin_user:
                        category.user_id = admin_user
                        needs_update = True
                    
                    if needs_update:
                        category.save()
                        self.stdout.write(self.style.WARNING(f"Updated existing category: {category.name} (ID: {category.id}) parent/user."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Category already exists: {category.name} (ID: {category.id})"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Created category: {category.name} (child of {parent_category.name}) (ID: {category.id})"))
                
                created_categories[cat_data["id"]] = category # Update map with the actual instance

        self.stdout.write(self.style.SUCCESS("Categories seeding completed successfully!"))
