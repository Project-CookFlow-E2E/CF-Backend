# seed.py
import os
import django
import datetime

# Configure Django settings BEFORE importing any models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Now we can safely import Django models
from django.contrib.auth import get_user_model
from users.models.favorite import Favorite
from shopping.models.shoppingListItem import ShoppingListItem
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.step import Step
from recipes.models.category import Category
from media.models.image import Image
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType

User = get_user_model()

def run():
    print("Clearing old data...")
    # Clear in reverse dependency order
    RecipeIngredient.objects.all().delete()
    Step.objects.all().delete()
    ShoppingListItem.objects.all().delete()
    Favorite.objects.all().delete()
    Recipe.objects.all().delete()
    Ingredient.objects.all().delete()
    Category.objects.all().delete()
    Unit.objects.all().delete()
    UnitType.objects.all().delete()
    Image.objects.all().delete()
    User.objects.all().delete()

    print("Creating unit types...")
    unit_type_count = UnitType.objects.create(name='Count')
    unit_type_mass = UnitType.objects.create(name='Mass')
    unit_type_volume = UnitType.objects.create(name='Volume')

    print("Creating users with media...")
    # Admin user for system-owned objects
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass',
        name='Admin',
        surname='System',
        second_surname='User',
        biography='System administrator account'
    )
    
    # Create profile images
    user1_img = Image.objects.create(
        name='john_profile',
        type=Image.ImageType.USER,
        url='media/users/john.jpg',
        processing_status=Image.ImageStatus.COMPLETED,
        external_id=1,
        created_at=datetime.datetime.now()
    )
    
    user2_img = Image.objects.create(
        name='jane_profile',
        type=Image.ImageType.USER,
        url='media/users/jane.jpg',
        processing_status=Image.ImageStatus.COMPLETED,
        external_id=2,
        created_at=datetime.datetime.now()
    )

    # Regular users
    user1 = User.objects.create_user(
        username='john_doe',
        email='john@example.com',
        password='password123',
        name='John',
        surname='Doe',
        second_surname='Smith',
        biography='Food lover and home cook'
    )
    user1.profile_image = user1_img
    user1.save()
    
    user2 = User.objects.create_user(
        username='jane_roe',
        email='jane@example.com',
        password='password123',
        name='Jane',
        surname='Roe',
        second_surname='Brown',
        biography='Recipe collector'
    )
    user2.profile_image = user2_img
    user2.save()

    print("Creating units...")
    unit_pieces = Unit.objects.create(
        name='Pieces',
        unit_type=unit_type_count,
        user_id=admin
    )
    unit_grams = Unit.objects.create(
        name='Grams',
        unit_type=unit_type_mass,
        user_id=admin
    )
    unit_cups = Unit.objects.create(
        name='Cups',
        unit_type=unit_type_volume,
        user_id=admin
    )

    print("Creating categories...")
    fruit_category = Category.objects.create(
        name='Fruits',
        user_id=admin
    )
    baking_category = Category.objects.create(
        name='Baking',
        user_id=admin
    )

    print("Creating ingredients with media...")
    # Create ingredient images
    apple_img = Image.objects.create(
        name='apple_ingredient',
        type='INGREDIENT',
        url='media/ingredients/apple.jpg',
        processing_status=Image.ImageStatus.COMPLETED,
        external_id=3,
        created_at=datetime.datetime.now()
    )
    flour_img = Image.objects.create(
        name='flour_ingredient',
        type='INGREDIENT',
        url='media/ingredients/flour.jpg',
        processing_status=Image.ImageStatus.COMPLETED,
        external_id=4,
        created_at=datetime.datetime.now()
    )

    ingredient1 = Ingredient.objects.create(
        name='Apple',
        user_id=admin,
        unit_type_id=unit_type_count,
        is_approved=True
    )
    ingredient1.ingredient_image = apple_img
    ingredient1.save()
    ingredient1.categories.add(fruit_category)
    
    ingredient2 = Ingredient.objects.create(
        name='Flour',
        user_id=admin,
        unit_type_id=unit_type_mass,
        is_approved=True
    )
    ingredient2.ingredient_image = flour_img
    ingredient2.save()
    ingredient2.categories.add(baking_category)
    
    ingredient3 = Ingredient.objects.create(
        name='Sugar',
        user_id=admin,
        unit_type_id=unit_type_mass,
        is_approved=True
    )
    ingredient3.categories.add(baking_category)

    print("Creating recipes with media...")
    # Create recipe images
    pie_img = Image.objects.create(
        name='apple_pie',
        type=Image.ImageType.RECIPE,
        url='media/recipes/apple_pie.jpg',
        processing_status=Image.ImageStatus.COMPLETED,
        external_id=5,
        created_at=datetime.datetime.now()
    )
    cookies_img = Image.objects.create(
        name='sugar_cookies',
        type=Image.ImageType.RECIPE,
        url='media/recipes/sugar_cookies.jpg',
        processing_status=Image.ImageStatus.COMPLETED,
        external_id=6,
        created_at=datetime.datetime.now()
    )

    recipe1 = Recipe.objects.create(
        name='Apple Pie',
        description='Delicious homemade apple pie.',
        user_id=user1,
        duration_minutes=60,
        commensals=8
    )
    recipe1.recipe_image = pie_img
    recipe1.save()
    recipe1.categories.add(fruit_category, baking_category)
    
    recipe2 = Recipe.objects.create(
        name='Sugar Cookies',
        description='Sweet and crunchy sugar cookies.',
        user_id=user2,
        duration_minutes=30,
        commensals=24
    )
    recipe2.recipe_image = cookies_img
    recipe2.save()
    recipe2.categories.add(baking_category)

    print("Creating recipe ingredients...")
    RecipeIngredient.objects.create(
        recipe=recipe1,
        ingredient=ingredient1,
        quantity=4,
        unit='Pieces'
    )
    RecipeIngredient.objects.create(
        recipe=recipe1,
        ingredient=ingredient2,
        quantity=300,
        unit='Grams'
    )
    RecipeIngredient.objects.create(
        recipe=recipe2,
        ingredient=ingredient3,
        quantity=200,
        unit='Grams'
    )

    print("Creating steps...")
    Step.objects.create(
        order=1,
        recipe_id=recipe1,
        description='Peel and slice the apples'
    )
    Step.objects.create(
        order=2,
        recipe_id=recipe1,
        description='Mix with flour and sugar'
    )

    print("Adding favorites...")
    Favorite.objects.create(user_id=user1, recipe_id=recipe1)
    Favorite.objects.create(user_id=user2, recipe_id=recipe2)

    print("Adding shopping list items...")
    ShoppingListItem.objects.create(
        user_id=user1,
        ingredient_id=ingredient1,
        quantity_needed=4,
        unit='Pieces',
        is_purchased=False
    )
    ShoppingListItem.objects.create(
        user_id=user2,
        ingredient_id=ingredient2,
        quantity_needed=500,
        unit='Grams',
        is_purchased=True
    )

    print("Seeding complete!")

if __name__ == '__main__':
    run()