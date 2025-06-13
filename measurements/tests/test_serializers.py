import pytest
from rest_framework.exceptions import ValidationError
from model_bakery import baker
from django.utils import timezone # Needed for datetime comparisons in tests

# CORRECTED IMPORTS: Ensure these point to the specific model files
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType 
from measurements.serializers.unitSerializer import UnitSerializer, UnitAdminSerializer
from measurements.serializers.unitTypeSerializer import UnitTypeSerializer, UnitTypeAdminSerializer
from users.models.user import CustomUser


@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.measurements_app
class TestUnitTypeSerializers:
    """
    Tests for UnitTypeSerializer and UnitTypeAdminSerializer.
    """

    def test_unittype_serializer_serialization(self, db):
        """
        Tests UnitTypeSerializer for correct serialization, including nested units (without IDs).
        """
        unittype = baker.make(UnitType, name='Weight')
        user1 = baker.make(CustomUser, username='user1') # Shortened username
        unit1 = baker.make(Unit, name='Kilogram', unit_type=unittype, user_id=user1)
        unit2 = baker.make(Unit, name='Gram', unit_type=unittype, user_id=user1) # Re-used user1

        serializer = UnitTypeSerializer(instance=unittype)
        expected_data = {
            # 'id' is NOT included for UnitTypeSerializer as per requirements for user visualization
            'name': 'Weight',
            'units': [
                # 'id' is NOT included for nested UnitSerializer as per requirements for user visualization
                {'name': 'Kilogram', 'unit_type': unittype.id}, 
                {'name': 'Gram', 'unit_type': unittype.id},
            ]
        }
        
        # Sort units by 'name' for consistent comparison now that 'id' is not available in expected data
        serializer_units_sorted = sorted(serializer.data['units'], key=lambda x: x['name'])
        expected_units_sorted = sorted(expected_data['units'], key=lambda x: x['name'])
        
        assert 'id' not in serializer.data # Explicitly check that UnitType ID is NOT present
        assert serializer.data['name'] == expected_data['name']
        assert serializer_units_sorted == expected_units_sorted

    def test_unittype_serializer_read_only_fields(self, db):
        """
        Tests that UnitTypeSerializer fields ('name', 'units') are read-only.
        """
        unittype = baker.make(UnitType, name='OldType') # Shortened name
        # Attempt to modify read-only fields
        data = {'name': 'New Type', 'units': [{'name': 'FakeUnit', 'unit_type': 0}]} 
        serializer = UnitTypeSerializer(instance=unittype, data=data, partial=True)
        
        # is_valid should pass because read-only fields are ignored for input
        assert serializer.is_valid(raise_exception=True)
        updated_unittype = serializer.save()
        
        # Ensure read-only fields are not updated
        assert updated_unittype.name == unittype.name # Name should not change
        assert updated_unittype.units.count() == unittype.units.count() # Units list should not change via this serializer


    def test_unittype_admin_serializer_serialization(self, db):
        """
        Tests UnitTypeAdminSerializer for correct read-only serialization of all fields.
        """
        # Ensure a created_at field is present for comparison
        unittype = baker.make(UnitType, name='AdmType', created_at=timezone.now()) # Shortened name
        serializer = UnitTypeAdminSerializer(instance=unittype)
        
        # Expect all direct model fields, formatted as they would be by DRF
        expected_data = {
            'id': unittype.id,
            'name': 'AdmType',
            'created_at': unittype.created_at.isoformat().replace('+00:00', 'Z') # Format datetime for comparison
        }
        
        # Check that all expected fields are present and match.
        assert 'id' in serializer.data
        assert 'name' in serializer.data
        assert 'created_at' in serializer.data
        
        assert serializer.data['id'] == expected_data['id']
        assert serializer.data['name'] == expected_data['name']
        assert serializer.data['created_at'].startswith(expected_data['created_at'][:19]) 

    def test_unittype_admin_serializer_is_fully_read_only(self, db):
        """
        Tests that UnitTypeAdminSerializer rejects any write attempts (create or update).
        """
        # Clean slate for this specific test's counting
        UnitType.objects.all().delete()
        initial_db_count = UnitType.objects.count() # Should be 0 here

        # Scenario 1: Attempt to update an existing UnitType
        # Ensure name respects max_length=15 for baker.make
        unittype_instance_for_update = baker.make(UnitType, name='OrgTypeUT') # Length 10 <= 15
        
        # Test data for update (name needs to be <= 15 chars)
        data_update = {'name': 'UpdtdTypeUT', 'created_at': timezone.now().isoformat()} # Length 11 <= 15
        serializer_update = UnitTypeAdminSerializer(instance=unittype_instance_for_update, data=data_update, partial=True)
        
        assert serializer_update.is_valid(raise_exception=True) 
        # The ValidationError from the `update` method is now expected here
        with pytest.raises(ValidationError) as excinfo:
            serializer_update.save() 
        assert "This serializer is read-only; updates are not allowed." in excinfo.value.detail[0] # Changed for list of errors

        # Assert database count has not increased due to update attempt
        assert UnitType.objects.count() == initial_db_count + 1 # Still just the one object from baker.make


        # Scenario 2: Attempt to create a new UnitType
        # Test data for creation (name needs to be <= 15 chars)
        data_create = {'name': 'NewTypeAtmpt'} # Length 12 <= 15
        serializer_create = UnitTypeAdminSerializer(data=data_create)
        
        assert serializer_create.is_valid(raise_exception=True) # Data might be valid, but saving should fail
        # The ValidationError from the `create` method is now expected here
        with pytest.raises(ValidationError) as excinfo:
            serializer_create.save()
        assert "This serializer is read-only; creation is not allowed." in excinfo.value.detail[0]

        # No new object should be created by the serializer's save() method
        assert UnitType.objects.count() == initial_db_count + 1 # Still just the one object from baker.make
                                                               # No new object from serializer.save()


@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.measurements_app
class TestUnitSerializers:
    """
    Tests for UnitSerializer and UnitAdminSerializer.
    """

    def test_unit_serializer_serialization(self, db):
        """
        Tests UnitSerializer for correct serialization (without 'id').
        """
        unittype = baker.make(UnitType, name='TimeUT') # Shortened name
        user = baker.make(CustomUser, username='user_time') # Shortened username
        unit = baker.make(Unit, name='Second', unit_type=unittype, user_id=user)

        serializer = UnitSerializer(instance=unit)
        expected_data = {
            # 'id' is NOT included for UnitSerializer as per requirements for user visualization
            'name': 'Second',
            'unit_type': unittype.id, # unit_type is serialized as ID
        }
        # Assert individual fields, as 'id' is no longer in expected_data
        assert serializer.data['name'] == expected_data['name']
        assert serializer.data['unit_type'] == expected_data['unit_type']
        assert 'id' not in serializer.data # Explicitly check that 'id' is NOT present

    def test_unit_serializer_read_only_fields(self, db):
        """
        Tests that UnitSerializer fields ('name', 'unit_type') are read-only.
        """
        unittype = baker.make(UnitType, name='TypeForUnit') # Shortened name
        user = baker.make(CustomUser, username='user_meter') # Shortened username
        unit = baker.make(Unit, name='Meter', unit_type=unittype, user_id=user)

        # Attempt to modify read-only fields (no 'id' in data for this serializer)
        data = {'name': 'Foot', 'unit_type': baker.make(UnitType, name='FootType').id} # Shortened name
        serializer = UnitSerializer(instance=unit, data=data, partial=True)
        
        assert serializer.is_valid(raise_exception=True)
        updated_unit = serializer.save()
        
        # Ensure read-only fields are not updated
        assert updated_unit.name == unit.name # Name should not change
        assert updated_unit.unit_type == unit.unit_type # Unit type should not change

    def test_unit_admin_serializer_serialization(self, db):
        """
        Tests UnitAdminSerializer for correct read-only serialization of all fields.
        """
        # Ensure names respect max_length=15
        unittype = baker.make(UnitType, name='AdmUType') 
        user = baker.make(CustomUser, username="adm_unit_user")
        unit = baker.make(Unit, name='AdmUnit', unit_type=unittype, user_id=user, created_at=timezone.now())

        serializer = UnitAdminSerializer(instance=unit)
        expected_data = {
            'id': unit.id,
            'name': 'AdmUnit',
            'unit_type': unittype.id,
            'user_id': user.id,
            'created_at': unit.created_at.isoformat().replace('+00:00', 'Z')
        }

        # Check that all expected fields are present and match.
        assert 'id' in serializer.data
        assert 'name' in serializer.data
        assert 'unit_type' in serializer.data
        assert 'user_id' in serializer.data
        assert 'created_at' in serializer.data
        
        assert serializer.data['id'] == expected_data['id']
        assert serializer.data['name'] == expected_data['name']
        assert serializer.data['unit_type'] == expected_data['unit_type']
        assert serializer.data['user_id'] == expected_data['user_id']
        assert serializer.data['created_at'].startswith(expected_data['created_at'][:19]) # Compare up to seconds


    def test_unit_admin_serializer_is_fully_read_only(self, db):
        """
        Tests that UnitAdminSerializer rejects any write attempts (create or update).
        """
        # Clean slate for this specific test's counting
        Unit.objects.all().delete()
        initial_db_count = Unit.objects.count() # Should be 0 here

        # Scenario 1: Attempt to update an existing Unit
        # Ensure names respect max_length=15 for baker.make
        unittype = baker.make(UnitType, name='OrgUTypeForU') # Shortened name
        user = baker.make(CustomUser, username="org_user_for_u") # Shortened username
        unit_instance_for_update = baker.make(Unit, name='OrgUnitU', unit_type=unittype, user_id=user) # Shortened name
        
        # Attempt to update an existing Unit
        # Ensure names respect max_length=15
        data_update = {
            'name': 'Updt UnitU', # Shortened name
            'unit_type': baker.make(UnitType, name='NewUTypeForU').id, # Shortened name
            'user_id': baker.make(CustomUser, username="new_user_for_u").id # Shortened username
        }
        serializer_update = UnitAdminSerializer(instance=unit_instance_for_update, data=data_update, partial=True)
        
        assert serializer_update.is_valid(raise_exception=True) 
        with pytest.raises(ValidationError) as excinfo:
            updated_unit = serializer_update.save()
        assert "This serializer is read-only; updates are not allowed." in excinfo.value.detail[0]


        # No new object should be created by the serializer's save() method
        assert Unit.objects.count() == initial_db_count + 1 # Still just the one object from baker.make

        # Scenario 2: Attempt to create a new Unit
        # Ensure names respect max_length=15
        data_create = {
            'name': 'New Unt AtmptU', # Shortened name
            'unit_type': baker.make(UnitType, name='AnoUTypeForU').id, 
            'user_id': baker.make(CustomUser, username="ano_user_for_u").id 
        }
        serializer_create = UnitAdminSerializer(data=data_create)
        
        assert serializer_create.is_valid(raise_exception=True)
        with pytest.raises(ValidationError) as excinfo:
            new_unit_returned_by_save = serializer_create.save()
        assert "This serializer is read-only; creation is not allowed." in excinfo.value.detail[0]

        # No new object should be created by the serializer's save() method
        assert Unit.objects.count() == initial_db_count + 1 # Still just the one object from baker.make
