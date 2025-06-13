# cookflow-backend/conftest.py
import pytest
from model_bakery import baker
from users.models.user import CustomUser
from measurements.models.unitType import UnitType
from measurements.models.unit import Unit
from recipes.models.category import Category
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.step import Step
from media.models.image import Image


# --- User Fixtures ---
@pytest.fixture
def test_user_data():
    """Returns a dictionary of valid user data for creation."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'StrongPassword123!',
        'name': 'Test',
        'surname': 'User',
        'second_surname': 'Fixture'
    }

@pytest.fixture
def other_user_data():
    """Returns a dictionary for another valid user."""
    return {
        'username': 'otheruser',
        'email': 'other@example.com',
        'password': 'AnotherStrongPassword123!',
        'name': 'Other',
        'surname': 'Person',
        'second_surname': 'Here'
    }

@pytest.fixture(scope='function')
def test_user(db, test_user_data):
    """Creates and returns a regular CustomUser instance."""
    user = CustomUser.objects.create_user(**test_user_data)
    user.plain_password = test_user_data['password']
    return user

@pytest.fixture(scope='function')
def another_custom_user(db, other_user_data):
    """Creates and returns another regular CustomUser instance."""
    user = CustomUser.objects.create_user(**other_user_data)
    user.plain_password = other_user_data['password']
    return user

@pytest.fixture(scope='function')
def test_superuser(db):
    """Creates and returns a superuser CustomUser instance."""
    superuser_data = {
        'username': 'adminuser',
        'email': 'admin@example.com',
        'password': 'AdminPassword123!',
        'name': 'Admin',
        'surname': 'User',
        'second_surname': 'Account'
    }
    superuser = CustomUser.objects.create_superuser(**superuser_data)
    superuser.plain_password = superuser_data['password']
    return superuser

# --- Measurements App Fixtures ---
@pytest.fixture(scope='function')
def test_unit_type(db):
    """Creates and returns a common UnitType instance."""
    return baker.make(UnitType, name='TestUnitType')

@pytest.fixture(scope='function')
def test_unit(db, test_unit_type, test_user):
    """Creates and returns a common Unit instance."""
    return baker.make(Unit, name='TestUnit', unit_type=test_unit_type, user_id=test_user)

# --- Recipes App Fixtures ---
@pytest.fixture(scope='function')
def test_category(db, test_user):
    """Creates and returns a common Category instance."""
    return baker.make(Category, name='TestCategory', user_id=test_user)

@pytest.fixture(scope='function')
def test_ingredient(db, test_user, test_unit_type):
    """Creates and returns a common Ingredient instance."""
    return baker.make(Ingredient, name='TestIngredient', user_id=test_user, unit_type_id=test_unit_type)

@pytest.fixture(scope='function')
def test_recipe(db, test_user):
    """Creates and returns a common Recipe instance."""
    return baker.make(Recipe, name='Test Recipe', user_id=test_user, duration_minutes=30, commensals=4)

@pytest.fixture(scope='function')
def test_recipe_ingredient(db, test_recipe, test_ingredient, test_unit):
    """Creates and returns a common RecipeIngredient instance."""
    return baker.make(RecipeIngredient, recipe=test_recipe, ingredient=test_ingredient, quantity=100, unit=test_unit)

@pytest.fixture(scope='function')
def test_step(db, test_recipe):
    """Creates and returns a common Step instance."""
    return baker.make(Step, recipe=test_recipe, order=1, description='Test step description')

@pytest.fixture(scope='function')
def test_image(db, test_recipe): # Assuming image links to recipe via external_id
    """Creates and returns a common Image instance related to a recipe."""
    return baker.make(Image, external_id=test_recipe.id, type='RECIPE', url='http://example.com/test_recipe_image.jpg')

