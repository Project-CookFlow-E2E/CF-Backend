# users/tests/test_models.py
import pytest
from django.db import IntegrityError
from model_bakery import baker
from users.models.user import CustomUser
from users.models.favorite import Favorite


# Apply markers to the test class
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.users_app
class TestCustomUserModels:
    """
    Tests for the CustomUser model and CustomUserManager.
    Uses pytest.mark.django_db for database access.
    """

    def test_create_user_success(self, db, test_user_data):
        """
        Tests successful creation of a regular user.
        Verifies that the user is created and password is hashed.
        Uses test_user_data fixture.
        """
        user = CustomUser.objects.create_user(**test_user_data)

        assert user.username == test_user_data['username']
        assert user.email == test_user_data['email']
        assert user.name == test_user_data['name']
        assert user.surname == test_user_data['surname']
        assert user.second_surname == test_user_data['second_surname']
        assert not user.is_staff
        assert not user.is_superuser
        assert user.check_password(test_user_data['password'])
        assert CustomUser.objects.count() == 1


    def test_create_user_no_email_raises_error(self, db, test_user_data):
        """
        Tests that creating a user without an email raises a ValueError.
        """
        invalid_data = test_user_data.copy()
        invalid_data['email'] = '' # Empty email
        with pytest.raises(ValueError, match='El email es obligatorio'):
            CustomUser.objects.create_user(**invalid_data)

    def test_create_user_duplicate_username_raises_error(self, db, test_user):
        """
        Tests that creating a user with a duplicate username raises an IntegrityError.
        Uses test_user fixture to create an existing user.
        """
        with pytest.raises(IntegrityError):
            CustomUser.objects.create_user(
                username=test_user.username,  # Duplicate username
                email='second_dup@example.com',
                password='password123',
                name='Second',
                surname='User',
                second_surname='B'
            )

    def test_create_user_duplicate_email_raises_error(self, db, test_user):
        """
        Tests that creating a user with a duplicate email raises an IntegrityError.
        Uses test_user fixture to create an existing user.
        """
        with pytest.raises(IntegrityError):
            CustomUser.objects.create_user(
                username='usertwo_dup_email',
                email=test_user.email,  # Duplicate email
                password='password123',
                name='User',
                surname='Two',
                second_surname='Beta'
            )

    def test_create_superuser_success(self, db, test_superuser):
        """
        Tests successful creation of a superuser.
        Verifies is_staff and is_superuser are True.
        Uses test_superuser fixture.
        """
        assert test_superuser.username == 'adminuser'
        assert test_superuser.email == 'admin@example.com'
        assert test_superuser.is_staff
        assert test_superuser.is_superuser
        assert test_superuser.check_password('AdminPassword123!')

    def test_create_superuser_is_superuser_false_raises_error(self, db):
        """
        Tests that creating a superuser with is_superuser=False raises a ValueError.
        """
        with pytest.raises(ValueError, match='El superusuario debe tener is_superuser=True.'):
            CustomUser.objects.create_superuser(
                username='badadmin',
                email='bad@example.com',
                password='password123',
                is_superuser=False,  # Intentionally set to False
                name='Bad',
                surname='Admin',
                second_surname='User'
            )

    def test_create_superuser_is_staff_false_raises_error(self, db):
        """
        Tests that creating a superuser with is_staff=False raises a ValueError.
        """
        with pytest.raises(ValueError, match='El superusuario debe tener is_staff=True.'):
            CustomUser.objects.create_superuser(
                username='anotherbadadmin',
                email='anotherbad@example.com',
                password='password123',
                is_staff=False,  # Intentionally set to False
                name='Another Bad',
                surname='Admin',
                second_surname='User'
            )

    def test_customuser_field_null_false(self, db):
        """
        Tests that required fields cannot be null.
        This often manifests as IntegrityError or ValidationError depending on context.
        """
        # Testing a field that is null=False
        with pytest.raises(IntegrityError):
            CustomUser.objects.create(
                username='nulltest',
                email='null@example.com',
                password='password123',
                name='Null',
                surname='Test',
                second_surname=None # This will fail because second_surname is null=False
            )

    def test_customuser_biography_can_be_null_or_blank(self, db, test_user_data):
        """
        Tests that the 'biography' field can be null or blank.
        """
        user_data_null_bio = test_user_data.copy()
        user_data_null_bio['username'] = 'userwithnullbio'
        user_data_null_bio['email'] = 'nullbio@example.com'
        user_data_null_bio['biography'] = None
        user_with_null_bio = CustomUser.objects.create_user(**user_data_null_bio)
        assert user_with_null_bio.biography is None

        user_data_blank_bio = test_user_data.copy()
        user_data_blank_bio['username'] = 'userwithblankbio'
        user_data_blank_bio['email'] = 'blankbio@example.com'
        user_data_blank_bio['biography'] = ''
        user_with_blank_bio = CustomUser.objects.create_user(**user_data_blank_bio)
        assert user_with_blank_bio.biography == ''

    def test_customuser_auto_now_add_created_at(self, db):
        """
        Tests that 'created_at' is automatically set on creation.
        """
        user = baker.make(CustomUser)
        assert user.created_at is not None

    def test_customuser_auto_now_updated_at(self, db, test_user):
        """
        Tests that 'updated_at' is automatically updated on save.
        Uses test_user fixture.
        """
        old_updated_at = test_user.updated_at
        import time
        time.sleep(0.001)  # Ensure a slight time difference for update
        test_user.name = 'Updated Name'
        test_user.save()
        assert test_user.updated_at > old_updated_at


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.users_app
class TestFavoriteModels:
    """
    Tests for the Favorite model.
    """

    def test_favorite_creation_and_relationships(self, db, test_user, test_recipe):
        """
        Tests successful creation of a Favorite instance and its foreign key relationships.
        Uses test_user and test_recipe fixtures.
        """
        favorite = Favorite.objects.create(user_id=test_user, recipe_id=test_recipe)

        assert favorite.user_id == test_user
        assert favorite.recipe_id == test_recipe
        assert favorite.created_at is not None
        assert favorite.updated_at is not None
        assert Favorite.objects.count() == 1

    def test_favorite_auto_now_add_created_at(self, db, test_user, test_recipe):
        """
        Tests that 'created_at' is automatically set on creation for Favorite.
        Uses test_user and test_recipe fixtures.
        """
        favorite = baker.make(Favorite, user_id=test_user, recipe_id=test_recipe)
        assert favorite.created_at is not None

    def test_favorite_auto_now_updated_at(self, db, test_user, test_recipe):
        """
        Tests that 'updated_at' is automatically updated on save for Favorite.
        Uses test_user fixture.
        """
        favorite = baker.make(Favorite, user_id=test_user, recipe_id=test_recipe)
        old_updated_at = favorite.updated_at
        import time
        time.sleep(0.001)  # Ensure a slight time difference for update
        favorite.save()  # Saving without changing fields still triggers auto_now
        assert favorite.updated_at > old_updated_at
