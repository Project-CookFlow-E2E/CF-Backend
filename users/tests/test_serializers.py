# users/tests/test_serializers.py
import pytest
from rest_framework import serializers
from users.serializers.favoriteSerializer import FavoriteSerializer, FavoriteAdminSerializer
from users.serializers.userSerializer import (
    CustomUserSerializer,
    CustomUserAdminSerializer,
    CustomUserCreateSerializer,
    CustomUserLoginSerializer,
    CustomUserUpdateSerializer,
    CustomUserAdminUpdateSerializer,
    MyTokenObtainPairSerializer,
    CustomUserFrontSerializer
)
from users.models.user import CustomUser
from users.models.favorite import Favorite
from model_bakery import baker
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.users_app
class TestFavoriteSerializers:
    """
    Tests for FavoriteSerializer and FavoriteAdminSerializer.
    """

    def test_favorite_serializer_valid_data(self, db, test_user, test_recipe):
        """
        Tests serialization and deserialization with valid data for FavoriteSerializer.
        Uses test_user and test_recipe fixtures.
        """
        data = {
            'user_id': test_user.id,
            'recipe_id': test_recipe.id
        }
        serializer = FavoriteSerializer(data=data)
        assert serializer.is_valid(raise_exception=True)
        favorite = serializer.save()

        assert favorite.user_id == test_user
        assert favorite.recipe_id == test_recipe
        assert Favorite.objects.count() == 1

        # Test serialization (to_representation)
        retrieved_serializer = FavoriteSerializer(instance=favorite)
        assert retrieved_serializer.data['user_id'] == test_user.id
        assert retrieved_serializer.data['recipe_id'] == test_recipe.id
        assert 'id' in retrieved_serializer.data

    def test_favorite_serializer_invalid_data_missing_fields(self, db):
        """
        Tests deserialization with invalid data (missing required fields).
        """
        data = {} # Missing user_id and recipe_id
        serializer = FavoriteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'user_id' in serializer.errors
        assert 'recipe_id' in serializer.errors

    def test_favorite_serializer_invalid_data_non_existent_relations(self, db):
        """
        Tests deserialization with invalid data (non-existent foreign key IDs).
        """
        data = {
            'user_id': 999,  # Non-existent user ID
            'recipe_id': 888  # Non-existent recipe ID
        }
        serializer = FavoriteSerializer(data=data)
        assert not serializer.is_valid()
        assert 'user_id' in serializer.errors
        assert 'recipe_id' in serializer.errors
        assert 'Invalid pk' in str(serializer.errors['user_id'])
        assert 'Invalid pk' in str(serializer.errors['recipe_id'])

    def test_favorite_admin_serializer_valid_data(self, db, test_user, test_recipe):
        """
        Tests serialization and deserialization with valid data for FavoriteAdminSerializer.
        Uses test_user and test_recipe fixtures.
        """
        favorite = baker.make(Favorite, user_id=test_user, recipe_id=test_recipe)

        data = {
            'user_id': test_user.id,
            'recipe_id': test_recipe.id
        }
        serializer = FavoriteAdminSerializer(instance=favorite, data=data, partial=True)
        assert serializer.is_valid(raise_exception=True)
        updated_favorite = serializer.save()

        assert updated_favorite.user_id == test_user
        assert updated_favorite.recipe_id == test_recipe

        # Test serialization (to_representation)
        retrieved_serializer = FavoriteAdminSerializer(instance=updated_favorite)
        assert retrieved_serializer.data['user_id'] == test_user.id
        assert retrieved_serializer.data['recipe_id'] == test_recipe.id
        assert 'id' in retrieved_serializer.data
        assert 'created_at' in retrieved_serializer.data

    def test_favorite_admin_serializer_read_only_fields(self, db, test_user, test_recipe):
        """
        Tests that read_only_fields are not writable for FavoriteAdminSerializer.
        Uses test_user fixture.
        """
        favorite = baker.make(Favorite, user_id=test_user, recipe_id=test_recipe)

        initial_created_at = favorite.created_at
        data = {
            'id': 999,
            'created_at': '2023-01-01T00:00:00Z'
        }
        serializer = FavoriteAdminSerializer(instance=favorite, data=data, partial=True)
        assert serializer.is_valid(raise_exception=True)
        updated_favorite = serializer.save()

        assert updated_favorite.id == favorite.id
        assert updated_favorite.created_at == initial_created_at


@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.users_app
class TestCustomUserSerializers:
    """
    Tests for various CustomUser serializers.
    """

    def test_custom_user_serializer_serialization(self, db, test_user):
        """
        Tests CustomUserSerializer for correct serialization (read-only).
        Uses test_user fixture.
        """
        test_user.biography = 'A short bio'
        test_user.save()
        serializer = CustomUserSerializer(instance=test_user)

        expected_fields = [
            'id', 'username', 'email', 'name', 'surname',
            'second_surname', 'biography', 'created_at'
        ]
        assert set(serializer.data.keys()) == set(expected_fields)
        assert serializer.data['username'] == test_user.username
        assert serializer.data['email'] == test_user.email
        assert serializer.data['biography'] == test_user.biography

    def test_custom_user_admin_serializer_serialization(self, db, test_superuser):
        """
        Tests CustomUserAdminSerializer for correct serialization (all fields).
        Uses test_superuser fixture.
        """
        serializer = CustomUserAdminSerializer(instance=test_superuser)

        expected_fields = {
            'id', 'password', 'last_login', 'is_superuser', 'username',
            'email', 'is_staff', 'is_active', 
            'name', 'surname', 'second_surname', 'biography',
            'created_at', 'updated_at', 'groups', 'user_permissions'
        }

        assert set(serializer.data.keys()) == expected_fields
        assert serializer.data['is_staff'] == test_superuser.is_staff
        assert serializer.data['is_superuser'] == test_superuser.is_superuser
        assert serializer.data['is_active'] == test_superuser.is_active
        assert 'password' in serializer.data
        assert 'last_login' in serializer.data


    def test_custom_user_admin_serializer_read_only_fields(self, db, test_user):
        """
        Tests that read_only_fields are not writable for CustomUserAdminSerializer.
        Uses test_user fixture.
        """
        initial_created_at = test_user.created_at
        initial_updated_at = test_user.updated_at

        data = {
            'id': 999,
            'created_at': '2023-01-01T00:00:00Z',
            'updated_at': '2023-01-01T00:00:00Z'
        }
        serializer = CustomUserAdminSerializer(instance=test_user, data=data, partial=True)
        assert serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        assert updated_user.id == test_user.id
        assert updated_user.created_at == initial_created_at
        # The purpose of read_only_fields is that the serializer input for these fields is ignored.
        # The model's auto_now will still update 'updated_at' on save.
        assert updated_user.updated_at != initial_updated_at # Should be different due to auto_now


    def test_custom_user_create_serializer_valid_creation(self, db, other_user_data):
        """
        Tests CustomUserCreateSerializer for successful user creation.
        Uses other_user_data fixture for a fresh user.
        """
        data = other_user_data.copy()
        data['username'] = 'create_test_user'
        data['email'] = 'create_test@example.com'

        serializer = CustomUserCreateSerializer(data=data)
        assert serializer.is_valid(raise_exception=True)
        user = serializer.save()

        assert user.username == data['username']
        assert user.email == data['email']
        assert user.check_password(data['password'])
        assert CustomUser.objects.count() == 1

    def test_custom_user_create_serializer_invalid_missing_fields(self, db):
        """
        Tests CustomUserCreateSerializer for invalid data (missing required fields).
        """
        data = {
            'username': 'incomplete_user',
            'email': 'incomplete@example.com',
        }
        serializer = CustomUserCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors
        assert 'surname' in serializer.errors
        assert 'second_surname' in serializer.errors
        assert 'password' in serializer.errors

    def test_custom_user_create_serializer_duplicate_username(self, db, test_user):
        """
        Tests CustomUserCreateSerializer for duplicate username validation.
        Uses test_user fixture.
        """
        data = {
            'username': test_user.username,
            'email': 'another_dup@example.com',
            'name': 'Dup',
            'surname': 'User',
            'second_surname': 'Again',
            'password': 'password123',
        }
        serializer = CustomUserCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors
        assert 'already exists' in str(serializer.errors['username'])

    def test_custom_user_create_serializer_duplicate_email(self, db, test_user):
        """
        Tests CustomUserCreateSerializer for duplicate email validation.
        Uses test_user fixture.
        """
        data = {
            'username': 'user_dup_email_test',
            'email': test_user.email,
            'name': 'Another',
            'surname': 'User',
            'second_surname': 'Again',
            'password': 'password123',
        }
        serializer = CustomUserCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors
        assert 'already exists' in str(serializer.errors['email'])

    def test_custom_user_create_serializer_validate_password_strength(self, db):
        """
        Tests CustomUserCreateSerializer's password validation for strength.
        This relies on Django's password validation settings.
        """
        data = {
            'username': 'weakpassuser',
            'email': 'weakpass@example.com',
            'name': 'Weak',
            'surname': 'Pass',
            'second_surname': 'User',
            'password': 'abc',
        }
        serializer = CustomUserCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert any(err for err in serializer.errors['password'] if 'common' in err or 'short' in err)


    def test_custom_user_login_serializer_valid_credentials(self, db, test_user):
        """
        Tests CustomUserLoginSerializer with valid username/email and password.
        Uses test_user fixture's plain_password.
        """
        data_username = {'username': test_user.username, 'password': test_user.plain_password}
        data_email = {'username': test_user.email, 'password': test_user.plain_password}

        serializer_username = CustomUserLoginSerializer(data=data_username)
        assert serializer_username.is_valid(raise_exception=True)
        assert serializer_username.validated_data['user'] == test_user

        serializer_email = CustomUserLoginSerializer(data=data_email)
        assert serializer_email.is_valid(raise_exception=True)
        assert serializer_email.validated_data['user'] == test_user

    def test_custom_user_login_serializer_invalid_credentials(self, db, test_user):
        """
        Tests CustomUserLoginSerializer with invalid username/email or password.
        Uses test_user fixture.
        """
        data_wrong_pass = {'username': test_user.username, 'password': 'WrongPassword!'}
        serializer = CustomUserLoginSerializer(data=data_wrong_pass)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors
        assert "Credenciales inválidas." in str(serializer.errors['non_field_errors'])

        data_non_existent = {'username': 'nonexistent', 'password': 'AnyPassword!'}
        serializer = CustomUserLoginSerializer(data=data_non_existent)
        assert not serializer.is_valid()
        assert 'non_field_errors' in serializer.errors
        assert "Credenciales inválidas." in str(serializer.errors['non_field_errors'])

    def test_custom_user_login_serializer_inactive_user(self, db):
        """
        Tests CustomUserLoginSerializer for an inactive user.
        Creates a new inactive user for this test.
        """
        test_password = 'InactivePassword123!'

        # Create the user as inactive from the start using create_user
        inactive_user = CustomUser.objects.create_user(
            username='inactive_testuser',
            email='inactive@example.com',
            name='Inactive',
            surname='User',
            second_surname='Test',
            password=test_password,
            is_active=False # Set to inactive directly during creation
        )
        
        # Refresh from db is a good practice to ensure the Python object matches the DB state
        inactive_user.refresh_from_db()

        # Sanity check: Ensure the user is inactive after creation and refresh
        assert not inactive_user.is_active, "Test setup error: The user should be inactive after creation."

        # Sanity check: Explicitly fetch the user by PK to ensure DB state
        verified_inactive_user = CustomUser.objects.get(pk=inactive_user.pk)
        assert not verified_inactive_user.is_active, "DB state error: The verified user should be inactive."
        
        # Sanity check: Ensure the password is correct on the refreshed user object
        assert inactive_user.check_password(test_password), "Test setup error: Inactive user password verification failed."

        data = {'username': inactive_user.username, 'password': test_password}
        serializer = CustomUserLoginSerializer(data=data)
        
        with pytest.raises(serializers.ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        
        # Assert that the specific error message for inactive user is present
        assert "Usuario inactivo." in str(excinfo.value)


    def test_custom_user_update_serializer_valid_update(self, db, test_user):
        """
        Tests CustomUserUpdateSerializer for valid profile updates.
        Uses test_user fixture.
        """
        test_user.biography = 'Old bio'
        test_user.save()
        data = {
            'name': 'Updated Name',
            'biography': 'New bio content.'
        }
        serializer = CustomUserUpdateSerializer(instance=test_user, data=data, partial=True)
        assert serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        assert updated_user.name == 'Updated Name'
        assert updated_user.biography == 'New bio content.'
        assert updated_user.username == test_user.username
        assert updated_user.email == test_user.email

    def test_custom_user_update_serializer_password_update(self, db, test_user):
        """
        Tests CustomUserUpdateSerializer for password update.
        Uses test_user fixture.
        """
        old_password_hash = test_user.password
        data = {'password': 'NewStrongPassword123!'}
        serializer = CustomUserUpdateSerializer(instance=test_user, data=data, partial=True)
        assert serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        assert updated_user.check_password('NewStrongPassword123!')
        assert updated_user.password != old_password_hash

    def test_custom_user_update_serializer_invalid_password_update(self, db, test_user):
        """
        Tests CustomUserUpdateSerializer with invalid password update.
        Uses test_user fixture.
        """
        data = {'password': 'weak'}
        serializer = CustomUserUpdateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert any(err for err in serializer.errors['password'] if 'common' in err or 'short' in err)


    def test_custom_user_admin_update_serializer_valid_update(self, db, test_user):
        """
        Tests CustomUserAdminUpdateSerializer for admin-level updates.
        Uses test_user fixture.
        """
        test_user.is_staff = False
        test_user.biography = 'Old bio'
        test_user.save()

        data = {
            'username': 'admin_updated_user',
            'email': 'admin_updated@example.com',
            'name': 'Admin Updated',
            'is_staff': True,
            'biography': 'Admin sets new bio.'
        }
        serializer = CustomUserAdminUpdateSerializer(instance=test_user, data=data, partial=True)
        assert serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        assert updated_user.username == 'admin_updated_user'
        assert updated_user.email == 'admin_updated@example.com'
        assert updated_user.name == 'Admin Updated'
        assert updated_user.is_staff is True
        assert updated_user.biography == 'Admin sets new bio.'

    def test_custom_user_admin_update_serializer_password_update(self, db, test_user):
        """
        Tests CustomUserAdminUpdateSerializer for admin-level password update.
        Uses test_user fixture.
        """
        old_password_hash = test_user.password
        data = {'password': 'AdminSetPassword!@#'}
        serializer = CustomUserAdminUpdateSerializer(instance=test_user, data=data, partial=True)
        assert serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        assert updated_user.check_password('AdminSetPassword!@#')
        assert updated_user.password != old_password_hash


    def test_my_token_obtain_pair_serializer_get_token_claims(self, db, test_superuser):
        """
        Tests MyTokenObtainPairSerializer to ensure custom claims are added to the token.
        Uses test_superuser fixture.
        """
        token = MyTokenObtainPairSerializer.get_token(test_superuser)

        assert 'username' in token
        assert 'email' in token
        assert 'is_staff' in token
        assert 'is_superuser' in token
        assert 'is_active' in token

        assert token['username'] == test_superuser.username
        assert token['email'] == test_superuser.email
        assert token['is_staff'] == test_superuser.is_staff
        assert token['is_superuser'] == test_superuser.is_superuser
        assert token['is_active'] == test_superuser.is_active


    def test_custom_user_front_serializer_serialization(self, db, test_user):
        """
        Tests CustomUserFrontSerializer for minimal serialization (id, username).
        Uses test_user fixture.
        """
        serializer = CustomUserFrontSerializer(instance=test_user)

        expected_fields = ['id', 'username']
        assert set(serializer.data.keys()) == set(expected_fields)
        assert serializer.data['id'] == test_user.id
        assert serializer.data['username'] == test_user.username
        assert 'email' not in serializer.data
        assert 'name' not in serializer.data
