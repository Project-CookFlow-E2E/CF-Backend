# measurements/tests/test_models.py
import pytest
from django.db import IntegrityError, DataError
from model_bakery import baker
from measurements.models import Unit, UnitType
from users.models.user import CustomUser # Assuming Unit.user_id points to CustomUser
from django.utils import timezone


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.measurements_app
class TestUnitTypeModels:
    """
    Tests for the UnitType model.
    """

    def test_unittype_creation_success(self, db):
        """
        Tests successful creation of a UnitType instance.
        """
        unittype = UnitType.objects.create(name='Volume')
        assert unittype.name == 'Volume'
        assert unittype.created_at is not None
        assert UnitType.objects.count() == 1

    def test_unittype_duplicate_name_raises_error(self, db):
        """
        Tests that creating a UnitType with a duplicate name raises an IntegrityError.
        """
        UnitType.objects.create(name='Weight')
        with pytest.raises(IntegrityError):
            UnitType.objects.create(name='Weight')

    def test_unittype_name_too_long_raises_error(self, db):
        """
        Tests that UnitType name respects max_length constraint and raises DataError.
        This test only attempts to save an invalid name.
        """
        long_name = 'ThisNameIsTooLongFor15Characters' # 32 characters
        unittype = UnitType(name=long_name)
        with pytest.raises(DataError): # Explicitly catch DataError from database
            unittype.save()

    def test_unittype_name_valid_saves_successfully(self, db):
        """
        Tests that a UnitType with a valid name saves successfully.
        This test only attempts to save a valid name.
        """
        valid_name = 'FifteenChars' # 12 characters, valid
        unittype = UnitType(name=valid_name)
        unittype.save()
        assert unittype.name == valid_name
        assert UnitType.objects.filter(name=valid_name).exists()


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.measurements_app
class TestUnitModels:
    """
    Tests for the Unit model.
    """

    def test_create_unit_success(self, db):
        """
        Tests successful creation of a Unit instance.
        Ensures foreign key dependencies are met and created_at is set.
        """
        # Create necessary foreign key instances using baker
        unittype = baker.make(UnitType, name="DefaultUnitType")
        user = baker.make(CustomUser, username="unitcreator", email="unit@example.com", password="password")

        # Create Unit instance with all required fields
        unit = Unit.objects.create(
            name="gramo",
            unit_type=unittype,
            user_id=user
        )

        assert unit.id is not None
        assert unit.name == "gramo"
        assert unit.unit_type == unittype
        assert unit.user_id == user
        assert isinstance(unit.created_at, timezone.datetime)
        # Removed updated_at assertion as per your model definition.
    
    def test_unit_duplicate_name_raises_error(self, db):
        """
        Tests that creating a Unit with a duplicate name raises an IntegrityError.
        """
        unittype = baker.make(UnitType, name='Capacity')
        user = baker.make(CustomUser, username="user_dup_unit", email="dup_unit@example.com", password="password")
        Unit.objects.create(name='Liter', unit_type=unittype, user_id=user)
        with pytest.raises(IntegrityError):
            Unit.objects.create(name='Liter', unit_type=unittype, user_id=user)

    def test_unit_name_too_long_raises_error(self, db):
        """
        Tests that Unit name respects max_length constraint and raises DataError.
        This test only attempts to save an invalid name.
        """
        unittype = baker.make(UnitType, name='Mass')
        user = baker.make(CustomUser, username="user_long_name", email="long_name@example.com", password="password")
        long_name = 'ThisUnitNameIsTooLongFor15Characters' # 36 characters
        unit = Unit(name=long_name, unit_type=unittype, user_id=user)
        with pytest.raises(DataError): # Explicitly catch DataError
            unit.save()

    def test_unit_name_valid_saves_successfully(self, db):
        """
        Tests that a Unit with a valid name saves successfully.
        This test only attempts to save a valid name.
        """
        unittype = baker.make(UnitType, name='Length')
        user = baker.make(CustomUser, username="user_valid_name", email="valid_name@example.com", password="password")
        valid_name = 'Kilogram' # 8 characters, valid
        unit = Unit(name=valid_name, unit_type=unittype, user_id=user)
        unit.save()
        assert unit.name == valid_name
        assert Unit.objects.filter(name=valid_name).exists()

    def test_unit_foreign_key_on_delete_cascade(self, db):
        """
        Tests CASCADE behavior for unit_type when UnitType is deleted.
        """
        unittype = baker.make(UnitType, name='Temperature')
        user = baker.make(CustomUser, username="user_cascade", email="cascade@example.com", password="password")
        unit = Unit.objects.create(name='Celsius', unit_type=unittype, user_id=user)
        assert Unit.objects.count() == 1
        
        unittype.delete()
        assert Unit.objects.count() == 0 # Unit should be deleted

    def test_unit_foreign_key_on_delete_set_default(self, db):
        """
        Tests SET_DEFAULT behavior for user_id when CustomUser is deleted.
        Ensures a default user with ID=1 exists for the default behavior.
        """
        # Ensure a default user with ID=1 exists if your settings.AUTH_USER_MODEL default=1
        # It's good practice to create this in the test for isolation.
        default_user = CustomUser.objects.get_or_create(
            id=1,
            defaults={
                'username': 'default_system_user',
                'email': 'default@example.com',
                'password': 'DefaultPassword123!',
                'name': 'Default',
                'surname': 'System',
                'second_surname': 'User'
            }
        )[0] # get_or_create returns (object, created) tuple
        
        # Create a user to be deleted, and a unit associated with them
        user_to_delete = baker.make(CustomUser, username='user_to_delete_for_unit', email='delete_unit@example.com', password="password")
        unittype = baker.make(UnitType, name='Liquid')
        unit = Unit.objects.create(name='Gallon', unit_type=unittype, user_id=user_to_delete)
        
        assert unit.user_id == user_to_delete
        assert Unit.objects.filter(id=unit.id).exists() # Ensure unit exists before user deletion
        
        user_to_delete.delete()
        
        # Fetch the unit again to see the updated user_id
        unit.refresh_from_db()
        assert unit.user_id == default_user # Should now point to the default user (ID=1)
