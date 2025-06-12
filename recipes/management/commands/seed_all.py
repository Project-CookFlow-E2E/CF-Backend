from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Ejecuta todos los seeders en el orden correcto.'

    def handle(self, *args, **options):
        seeders = [
            'unitType_seeder',
            'users_seeder',
            'unit_seeder',
            'categories_seeder',
            'ingredient_seeder',
            'recipe_seeder',
            'recipeIngredient_seeder',
        ]

        for seeder in seeders:
            try:
                self.stdout.write(self.style.NOTICE(f"Ejecutando {seeder}..."))
                call_command(seeder)
                self.stdout.write(self.style.SUCCESS(f"✅ {seeder} completado."))
            except CommandError as e:
                self.stderr.write(self.style.ERROR(f"❌ Error al ejecutar {seeder}: {e}"))
                break
