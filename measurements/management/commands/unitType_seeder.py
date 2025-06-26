# measurements/management/commands/unitType_seeder.py
from django.core.management.base import BaseCommand
from measurements.models.unitType import UnitType 

class Command(BaseCommand):
    help = "Seed initial unit types into the database."

    def handle(self, *args, **options):
        # Lista de tipos de unidad iniciales con IDs específicos
        unit_types_data = [
            {"id": 1, "name": "peso"},
            {"id": 2, "name": "volumen"},
            {"id": 3, "name": "unitario"} # Keeping it as 'unitario'
        ]

        # Crea o actualiza los tipos de unidad con IDs específicos
        for unit_data in unit_types_data:
            unit_type, created = UnitType.objects.get_or_create(
                id=unit_data["id"],
                defaults={"name": unit_data["name"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created unit type: {unit_type.name} (ID: {unit_type.id})"))
            else:
                self.stdout.write(self.style.WARNING(f"Unit type already exists: {unit_type.name} (ID: {unit_type.id})"))

        self.stdout.write(self.style.SUCCESS("Unit types seeding completed successfully!"))