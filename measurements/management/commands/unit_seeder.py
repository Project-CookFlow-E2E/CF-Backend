# cf-backend/measurements/management/commands/unit_seeder.py
from django.core.management.base import BaseCommand
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed initial units into the database."

    def handle(self, *args, **options):
        self.stdout.write("Ejecutando unit_seeder...")

        # Obtiene el usuario por defecto (id=1), asumiendo que users_seeder ya lo creó
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("Error: Admin user (ID=1) not found. Run users_seeder first!"))
            return

        # Obtener los UnitTypes por ID (deben existir previamente)
        try:
            peso_type = UnitType.objects.get(id=1)
            volumen_type = UnitType.objects.get(id=2)
            unitario_type = UnitType.objects.get(id=3)
        except UnitType.DoesNotExist:
            self.stdout.write(self.style.ERROR("Error: UnitTypes not found. Run unitType_seeder first!"))
            return

        # Lista de unidades iniciales con sus tipos correspondientes (por ID)
        units_data = [
            {"name": "gramos", "unit_type_id": 1},
            {"name": "gram", "unit_type_id": 1},
            {"name": "kilogramos", "unit_type_id": 1},
            {"name": "kg", "unit_type_id": 1},
            {"name": "mililitros", "unit_type_id": 2},
            {"name": "ml", "unit_type_id": 2},
            {"name": "litros", "unit_type_id": 2},
            {"name": "cucharadas", "unit_type_id": 3},
            {"name": "cucharaditas", "unit_type_id": 3},
            {"name": "unidades", "unit_type_id": 3},
        ]

        # Mapeo de IDs a objetos UnitType
        unit_types_map = {
            1: peso_type,
            2: volumen_type,
            3: unitario_type,
        }

        # Crea o actualiza las unidades
        for unit_data in units_data:
            unit_type_obj = unit_types_map[unit_data["unit_type_id"]]
            
            unit, created = Unit.objects.get_or_create(
                name=unit_data["name"],
                defaults={
                    "unit_type": unit_type_obj,
                    "user_id": user, # Assign the fetched admin user
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created unit: {unit.name} -> UnitType: {unit_type_obj.name} (ID: {unit_type_obj.id})"
                    )
                )
            else:
                # If unit already exists, ensure its user_id and unit_type are correct
                if unit.unit_type != unit_type_obj or unit.user_id != user:
                    unit.unit_type = unit_type_obj
                    unit.user_id = user
                    unit.save()
                    self.stdout.write(self.style.WARNING(f"Updated existing unit: {unit.name} -> UnitType: {unit.unit_type.name} (ID: {unit.unit_type.id}) user/type."))
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Unit already exists: {unit.name} -> UnitType: {unit.unit_type.name} (ID: {unit.unit_type.id})"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Units seeding completed successfully!"))
