# from django.core.management.base import BaseCommand, CommandError
# from django.core.management import call_command

# class Command(BaseCommand):
#     help = 'Ejecuta todos los seeders en el orden correcto.'

#     def handle(self, *args, **options):
#         seeders = [
#             'unitType_seeder',
#             'users_seeder',
#             'unit_seeder',
#             'categories_seeder',
#             'ingredient_seeder',
#             'recipe_seeder',
#             'recipeIngredient_seeder',
#         ]

#         for seeder in seeders:
#             try:
#                 self.stdout.write(self.style.NOTICE(f"Ejecutando {seeder}..."))
#                 call_command(seeder)
#                 self.stdout.write(self.style.SUCCESS(f"✅ {seeder} completado."))
#             except CommandError as e:
#                 self.stderr.write(self.style.ERROR(f"❌ Error al ejecutar {seeder}: {e}"))
#                 break

# cookflow-backend/management/commands/seed_all.py
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.apps import apps # To get models dynamically

class Command(BaseCommand):
    help = 'Ejecuta todos los seeders en el orden correcto. Usa --reset para eliminar datos existentes antes de sembrar.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los datos existentes de los modelos sembrados antes de ejecutar los seeders.',
        )

    def _clear_data(self):
        self.stdout.write(self.style.WARNING("Iniciando eliminación de datos existentes..."))
        # Define the order of deletion to respect foreign key constraints
        # Delete models that depend on others first
        models_to_clear = [
            'recipes.RecipeIngredient', # Depends on Recipe, Ingredient, Unit
            'recipes.Step',             # Depends on Recipe
            'recipes.Recipe',           # Depends on CustomUser, Category
            'recipes.Ingredient',       # Depends on CustomUser, Category, UnitType
            'recipes.Category',         # Depends on CustomUser, self (parent)
            'measurements.Unit',        # Depends on CustomUser, UnitType
            'measurements.UnitType',
            'users.CustomUser',         # Should be last among app models if other models link to it
        ]

        for model_path in models_to_clear:
            try:
                app_label, model_name = model_path.split('.')
                Model = apps.get_model(app_label, model_name)
                count = Model.objects.count()
                if count > 0:
                    Model.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(f"Eliminados {count} registros de {model_name}."))
                else:
                    self.stdout.write(self.style.WARNING(f"No hay registros de {model_name} para eliminar."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error al eliminar datos de {model_path}: {e}"))
                raise # Re-raise to stop the process if deletion fails

        self.stdout.write(self.style.SUCCESS("Eliminación de datos completada."))

    def handle(self, *args, **options):
        if options['reset']:
            self._clear_data()

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
                break # Stop if a seeder fails
            except Exception as e: # Catch other exceptions during seeder execution
                self.stderr.write(self.style.ERROR(f"❌ Error inesperado al ejecutar {seeder}: {e}"))
                break
