from django.core.management.base import BaseCommand
from measurements.models.unitType import UnitType 

class Command(BaseCommand):
    help = "Seed initial unit types into the database."

    def handle(self, *args, **options):
        # Lista de tipos de unidad iniciales comunes en cocina
        unit_types_data = [
            {"name": "gramos"},
            {"name": "kilogramos"},
            {"name": "mililitros"},
            {"name": "litros"},
            {"name": "cucharadas"},
            {"name": "cucharaditas"},
            {"name": "unidades"}
        ]

        # Crea o actualiza los tipos de unidad
        for unit_data in unit_types_data:
            unit_type, created = UnitType.objects.get_or_create(
                name=unit_data["name"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created unit type: {unit_type.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Unit type already exists: {unit_type.name}"))

        self.stdout.write(self.style.SUCCESS("Unit types seeding completed successfully!"))