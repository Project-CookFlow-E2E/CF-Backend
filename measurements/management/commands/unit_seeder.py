# from django.core.management.base import BaseCommand
# from measurements.models.unit import Unit
# from measurements.models.unitType import UnitType  # Cambiado para coincidir con tu import
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Command(BaseCommand):
#     help = "Seed initial units into the database."

#     def handle(self, *args, **options):
#         # Obtiene o crea el usuario por defecto (id=1)
#         user, _ = User.objects.get_or_create(
#             id=1,
#             defaults={
#                 "username": "admin",
#                 "email": "admin@example.com",
#                 "name": "Admin",
#                 "surname": "Principal",
#                 "second_surname": "Root",
#                 "biography": "Super user of the system",
#                 "is_staff": True,
#                 "is_superuser": True,
#             },
#         )
#         if hasattr(user, 'set_password'):
#             user.set_password("admin12345")
#             user.save()

#         # Obtener los UnitTypes por ID (deben existir previamente)
#         try:
#             peso_type = UnitType.objects.get(id=1)        # peso
#             volumen_type = UnitType.objects.get(id=2)     # volumen  
#             unidades_type = UnitType.objects.get(id=3)    # unidades
#             unitario_type = UnitType.objects.get(id=4)    # unitario
#         except UnitType.DoesNotExist:
#             self.stdout.write(self.style.ERROR("Error: UnitTypes not found. Run unitType_seeder first!"))
#             return

#         # Lista de unidades iniciales con sus tipos correspondientes (por ID)
#         units_data = [
#             {"name": "gramos", "unit_type_id": 1},      # peso
#             {"name": "kilogramos", "unit_type_id": 1},  # peso
#             {"name": "mililitros", "unit_type_id": 2},  # volumen
#             {"name": "litros", "unit_type_id": 2},      # volumen
#             {"name": "cucharadas", "unit_type_id": 3},  # unidades
#             {"name": "cucharaditas", "unit_type_id": 3}, # unidades
#             {"name": "unidades", "unit_type_id": 4}     # unitario
#         ]

#         # Mapeo de IDs a objetos UnitType
#         unit_types_map = {
#             1: peso_type,
#             2: volumen_type,
#             3: unidades_type,
#             4: unitario_type
#         }

#         # Crea o actualiza las unidades
#         for unit_data in units_data:
#             unit_type_obj = unit_types_map[unit_data["unit_type_id"]]
            
#             unit, created = Unit.objects.get_or_create(
#                 name=unit_data["name"],
#                 defaults={
#                     "unit_type": unit_type_obj,
#                     "user_id": user,
#                 }
                
#             )
#             if created:
#                 self.stdout.write(
#                     self.style.SUCCESS(
#                         f"Created unit: {unit.name} -> UnitType: {unit_type_obj.name} (ID: {unit_type_obj.id})"
#                     )
#                 )
#             else:
#                 self.stdout.write(
#                     self.style.WARNING(
#                         f"Unit already exists: {unit.name} -> UnitType: {unit.unit_type.name} (ID: {unit.unit_type.id})"
#                     )
#                 )

#         self.stdout.write(self.style.SUCCESS("Units seeding completed successfully!"))


from django.core.management.base import BaseCommand
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed initial units into the database."

    def handle(self, *args, **options):
        # Obtiene o crea el usuario por defecto (id=1)
        user, _ = User.objects.get_or_create(
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
            },
        )
        if hasattr(user, 'set_password'):
            user.set_password("admin12345")
            user.save()
# Obtener los UnitTypes por ID (deben existir previamente)
        try:
            peso_type = UnitType.objects.get(id=1)        # peso
            volumen_type = UnitType.objects.get(id=2)     # volumen  
            unidades_type = UnitType.objects.get(id=3)    # unidades
            
        except UnitType.DoesNotExist:
            self.stdout.write(self.style.ERROR("Error: UnitTypes not found. Run unitType_seeder first!"))
            return

        # Lista de unidades iniciales con sus tipos correspondientes (por ID)
        units_data = [
            {"name": "gramos", "unit_type_id": 1},      # peso
            {"name": "kilogramos", "unit_type_id": 1},  # peso
            {"name": "mililitros", "unit_type_id": 2},  # volumen
            {"name": "litros", "unit_type_id": 2},      # volumen
            {"name": "cucharadas", "unit_type_id": 3},  # unidades
            {"name": "cucharaditas", "unit_type_id": 3}, # unitario
            {"name": "unidades", "unit_type_id": 3}     # unitario
        ]

        # Mapeo de IDs a objetos UnitType
        unit_types_map = {
            1: peso_type,
            2: volumen_type,
            3: unidades_type,
         
        }
# Crea o actualiza las unidades
        for unit_data in units_data:
            unit_type_obj = unit_types_map[unit_data["unit_type_id"]]
            
            unit, created = Unit.objects.get_or_create(
                name=unit_data["name"],
                defaults={
                    "unit_type": unit_type_obj,
                    "user_id": user,
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created unit: {unit.name} -> UnitType: {unit_type_obj.name} (ID: {unit_type_obj.id})"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Unit already exists: {unit.name} -> UnitType: {unit.unit_type.name} (ID: {unit.unit_type.id})"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Units seeding completed successfully!"))