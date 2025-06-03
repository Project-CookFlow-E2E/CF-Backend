import pytest
from django.db import IntegrityError
from core.models.User import CustomUser

@pytest.fixture
def user():
    """
    Fixture que crea un usuario con datos válidos para usar en los tests.
    """
    return CustomUser.objects.create(
        username='testusername',
        email='testusername@example.com',
        name='John',
        surname='Doe',
        second_surname='Smith',
        is_admin=False,
        biography='This is a test biography.'
    )

@pytest.mark.django_db
def test_username_unique(user):
    """
    Verifica que el campo 'username' sea único y no se puedan crear usuarios con el mismo username.
    Debe lanzar un error de integridad en la base de datos.
    """
    with pytest.raises(IntegrityError):
        CustomUser.objects.create(
            username='testusername',  # username duplicado
            email='differentemail@example.com',
            name='John',
            surname='Doe',
            second_surname='Smith',
            is_admin=False,
            biography='Another biography.'
        )

@pytest.mark.django_db
def test_email_unique(user):
    """
    Verifica que el campo 'email' sea único y no se puedan crear usuarios con el mismo email.
    Debe lanzar un error de integridad en la base de datos.
    """
    with pytest.raises(IntegrityError):
        CustomUser.objects.create(
            username='anotheruser',
            email='testusername@example.com',  # email duplicado
            name='John',
            surname='Doe',
            second_surname='Smith',
            is_admin=False,
            biography='Another biography.'
        )

@pytest.mark.django_db
def test_created_at_and_updated_at(user):
    """
    Comprueba que los campos 'created_at' y 'updated_at' se establecen automáticamente.
    """
    assert user.created_at is not None
    assert user.updated_at is not None

@pytest.mark.django_db
def test_is_admin_default(user):
    """
    Comprueba que el campo 'is_admin' por defecto sea False cuando se crea un usuario normal.
    """
    assert user.is_admin is False

@pytest.mark.django_db
def test_biography_nullable():
    """
    Verifica que el campo 'biography' sea opcional (nullable).
    Se debe poder crear un usuario sin biografía.
    """
    user_without_bio = CustomUser.objects.create(
        username='uniqueusername',
        email='uniqueemail@example.com',
        name='John',
        surname='Doe',
        second_surname='Smith',
        is_admin=False
    )
    assert user_without_bio.biography is None
