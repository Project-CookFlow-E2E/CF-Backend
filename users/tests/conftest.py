# users/tests/conftest.py
import pytest
from model_bakery import baker
from users.models.user import CustomUser


@pytest.fixture
def test_user_data():
    """
    Returns a dictionary of valid user data for creation.
    """
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
    """
    Returns a dictionary for another valid user.
    """
    return {
        'username': 'otheruser',
        'email': 'other@example.com',
        'password': 'AnotherStrongPassword123!',
        'name': 'Other',
        'surname': 'Person',
        'second_surname': 'Here'
    }


@pytest.fixture
def test_user(db, test_user_data):
    """
    Creates and returns a regular CustomUser instance, and stores its plain password.
    """
    user = CustomUser.objects.create_user(**test_user_data)
    user.plain_password = test_user_data['password'] # Store the plain password
    return user

@pytest.fixture
def test_superuser(db):
    """
    Creates and returns a superuser CustomUser instance, and stores its plain password.
    """
    superuser_data = {
        'username': 'adminuser',
        'email': 'admin@example.com',
        'password': 'AdminPassword123!',
        'name': 'Admin',
        'surname': 'User',
        'second_surname': 'Account'
    }
    superuser = CustomUser.objects.create_superuser(**superuser_data)
    superuser.plain_password = superuser_data['password'] # Store the plain password
    return superuser

@pytest.fixture
def test_recipe(db):
    """
    Creates and returns a dummy Recipe instance for testing Favorite model/serializer,
    since Favorite has a foreign key to Recipe.
    'recipes.Recipe' tells model_bakery to look in the 'recipes' app for the 'Recipe' model.
    """
    recipe = baker.make('recipes.Recipe', name='Test Recipe')
    return recipe

