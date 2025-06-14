from recipes.models import Category

# Los datos que se van a actualizar
categories_data = [
    {"id": 1, "name": "Categorias", "parent_category_id": None, "user_id": 1},
    {"id": 2, "name": "Tipo de cocina", "parent_category_id": None, "user_id": 1},
    {"id": 3, "name": "Origen", "parent_category_id": None, "user_id": 1},
    {"id": 4, "name": "Comida", "parent_category_id": 1, "user_id": 1},
    {"id": 5, "name": "Desayuno", "parent_category_id": 1, "user_id": 1},
    {"id": 6, "name": "Brunch", "parent_category_id": 1, "user_id": 1},
    {"id": 7, "name": "Cena", "parent_category_id": 1, "user_id": 1},
    {"id": 8, "name": "Postre", "parent_category_id": 1, "user_id": 1},
    {"id": 9, "name": "Merienda", "parent_category_id": 1, "user_id": 1},
    {"id": 10, "name": "Snack", "parent_category_id": 1, "user_id": 1},
    {"id": 11, "name": "Cocido", "parent_category_id": 2, "user_id": 1},
    {"id": 12, "name": "Al vapor", "parent_category_id": 2, "user_id": 1},
    {"id": 13, "name": "Hervido", "parent_category_id": 2, "user_id": 1},
    {"id": 14, "name": "Guiso", "parent_category_id": 2, "user_id": 1},
    {"id": 15, "name": "Frito", "parent_category_id": 2, "user_id": 1},
    {"id": 16, "name": "A la plancha", "parent_category_id": 2, "user_id": 1},
    {"id": 17, "name": "Asado", "parent_category_id": 2, "user_id": 1},
    {"id": 18, "name": "Sopas", "parent_category_id": 2, "user_id": 1},
    {"id": 19, "name": "Italiana", "parent_category_id": 3, "user_id": 1},
    {"id": 20, "name": "Griega", "parent_category_id": 3, "user_id": 1},
    {"id": 21, "name": "Española", "parent_category_id": 3, "user_id": 1},
    {"id": 22, "name": "Japonesa", "parent_category_id": 3, "user_id": 1},
    {"id": 23, "name": "Americana", "parent_category_id": 3, "user_id": 1}
]

# Recorrer cada categoría y actualizarla en la base de datos
for category_data in categories_data:
    category = Category.objects.get(id=category_data["id"])  # Obtiene la categoría por ID
    category.parent_category_id_id = category_data["parent_category_id"]  # Actualiza el parent_category_id
    category.user_id = category_data["user_id"]  # Actualiza el user_id
    category.save()  # Guarda la categoría actualizada

print("Categorías actualizadas correctamente.")
