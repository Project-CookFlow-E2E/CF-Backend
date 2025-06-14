import pytest
from rest_framework.exceptions import ValidationError
from model_bakery import baker
from django.utils import timezone 

# Import models
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType 
from measurements.serializers.unitSerializer import UnitSerializer, UnitAdminSerializer
from measurements.serializers.unitTypeSerializer import UnitTypeSerializer, UnitTypeAdminSerializer
from users.models.user import CustomUser # Used for creating users in tests when needed, or via test_user fixture


@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.measurements_app
class TestUnitTypeSerializers:
    """
    Tests for UnitTypeSerializer and UnitTypeAdminSerializer.
    """

    def test_unittype_serializer_serialization(self, test_user): # Uses global test_user fixture
        """
        Tests UnitTypeSerializer for correct serialization, including nested units.
        UnitSerializer is now expected to include 'id'.
        """
        unittype = baker.make(UnitType, name='WeightType') # Ensure name length is <=15
        
        # Create units using the test_user fixture
        unit1 = baker.make(Unit, name='Kilogram', unit_type=unittype, user_id=test_user)
        unit2 = baker.make(Unit, name='Gram', unit_type=unittype, user_id=test_user)

        serializer = UnitTypeSerializer(instance=unittype)
        expected_data = {
            # 'id' is NOT included for UnitTypeSerializer itself as per its fields definition
            'name': 'WeightType',
            'units': [
                # 'id' IS NOW included for nested UnitSerializer
                {'id': unit1.id, 'name': 'Kilogram', 'unit_type': unittype.id},
                {'id': unit2.id, 'name': 'Gram', 'unit_type': unittype.id},
            ]
        }
        
        # Sort units by 'name' for consistent comparison
        serializer_units_sorted = sorted(serializer.data['units'], key=lambda x: x['name'])
        expected_units_sorted = sorted(expected_data['units'], key=lambda x: x['name'])
        
        assert 'id' not in serializer.data # Explicitly check that UnitType ID is NOT present in root
        assert serializer.data['name'] == expected_data['name']
        assert serializer_units_sorted == expected_units_sorted

    def test_unittype_serializer_read_only_fields(self, test_user): # Uses global test_user fixture
        """
        Tests that UnitTypeSerializer fields ('name', 'units') are read-only for public users.
        """
        unittype = baker.make(UnitType, name='OldUnitType') 
        # Attempt to modify read-only fields
        data = {'name': 'New Type', 'units': [{'name': 'FakeUnit', 'unit_type': 0}]} 
        serializer = UnitTypeSerializer(instance=unittype, data=data, partial=True)
        
        assert serializer.is_valid(raise_exception=True)
        updated_unittype = serializer.save()
        
        # Ensure read-only fields are not updated
        assert updated_unittype.name == unittype.name # Name should not change
        assert updated_unittype.units.count() == unittype.units.count() # Units list should not change via this serializer


    def test_unittype_admin_serializer_serialization(self, test_unit_type, test_user): # Uses global fixture, added test_user for Unit creation
        """
        Tests UnitTypeAdminSerializer for correct read-only serialization of all fields, including units.
        """
        # Use the global fixture for a clean instance
        unittype = test_unit_type 
        # For comparison with created_at, ensure it's a datetime object
        unittype.created_at = timezone.now()
        unittype.save() # Save to update created_at for accurate comparison
        
        # Create some units related to this UnitType to test nested serialization
        unit1 = baker.make(Unit, name='KgAdmin', unit_type=unittype, user_id=test_user, created_at=timezone.now())
        unit2 = baker.make(Unit, name='gAdmin', unit_type=unittype, user_id=test_user, created_at=timezone.now())

        serializer = UnitTypeAdminSerializer(instance=unittype)
        data = serializer.data # Get serialized data

        # Expected nested unit data (sorted by name for consistent comparison)
        # CORRECTED: Include 'created_at' and 'user_id' in the expected nested data
        expected_units_data = sorted([
            {
                'id': unit1.id, 
                'name': 'KgAdmin', 
                'unit_type': unittype.id, 
                'user_id': test_user.id,
                'created_at': unit1.created_at.isoformat().replace('+00:00', 'Z')
            },
            {
                'id': unit2.id, 
                'name': 'gAdmin', 
                'unit_type': unittype.id, 
                'user_id': test_user.id,
                'created_at': unit2.created_at.isoformat().replace('+00:00', 'Z')
            },
        ], key=lambda x: x['name'])

        # Check that all expected fields are present and match.
        assert 'id' in data
        assert 'name' in data
        assert 'created_at' in data
        assert 'units' in data # Now explicitly asserting presence of 'units'
        
        assert data['id'] == unittype.id
        assert data['name'] == unittype.name
        # Compare up to seconds for datetime accuracy
        assert data['created_at'].startswith(unittype.created_at.isoformat().replace('+00:00', 'Z')[:19]) 
        assert isinstance(data['units'], list)
        
        # CORRECTED: Removed the problematic 'actual_units_data_cleaned' loop.
        # Now directly compare sorted lists item by item with datetime string comparison.
        actual_units_data_sorted = sorted(data['units'], key=lambda x: x['name'])
        
        assert len(actual_units_data_sorted) == len(expected_units_data)
        for i in range(len(actual_units_data_sorted)):
            assert actual_units_data_sorted[i]['id'] == expected_units_data[i]['id']
            assert actual_units_data_sorted[i]['name'] == expected_units_data[i]['name']
            assert actual_units_data_sorted[i]['unit_type'] == expected_units_data[i]['unit_type']
            assert actual_units_data_sorted[i]['user_id'] == expected_units_data[i]['user_id']
            # Compare created_at up to seconds by checking if the serialized string starts with the expected prefix
            actual_created_at_str = actual_units_data_sorted[i]['created_at']
            expected_created_at_prefix = expected_units_data[i]['created_at'][:19] # Get prefix like '2025-06-13T21:34:20'
            assert actual_created_at_str.startswith(expected_created_at_prefix)
            


    def test_unittype_admin_serializer_is_fully_read_only(self, test_unit_type): # Removed test_user from here as UnitType doesn't have user_id
        """
        Tests that UnitTypeAdminSerializer rejects any write attempts (create or update).
        """
        # Use a fresh UnitType for the update scenario (no user_id for UnitType)
        unittype_instance_for_update = baker.make(UnitType, name='OrgTypeUT')
        
        # Scenario 1: Attempt to update an existing UnitType
        data_update = {'name': 'UpdtdTypeUT'} 
        serializer_update = UnitTypeAdminSerializer(instance=unittype_instance_for_update, data=data_update, partial=True)
        
        assert serializer_update.is_valid(raise_exception=True) 
        with pytest.raises(ValidationError) as excinfo:
            serializer_update.save() 
        assert "This serializer is read-only; updates are not allowed." in excinfo.value.detail[0]

        # Ensure no change to the original object
        unittype_instance_for_update.refresh_from_db()
        assert unittype_instance_for_update.name == 'OrgTypeUT'


        # Scenario 2: Attempt to create a new UnitType
        data_create = {'name': 'NewTypeAtmpt'} 
        serializer_create = UnitTypeAdminSerializer(data=data_create)
        
        assert serializer_create.is_valid(raise_exception=True) 
        with pytest.raises(ValidationError) as excinfo:
            serializer_create.save()
        assert "This serializer is read-only; creation is not allowed." in excinfo.value.detail[0]

        # No new object should be created
        assert not UnitType.objects.filter(name='NewTypeAtmpt').exists()


@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.measurements_app
class TestUnitSerializers:
    """
    Tests for UnitSerializer and UnitAdminSerializer.
    """

    def test_unit_serializer_serialization(self, test_unit_type, test_user): # Uses global fixtures
        """
        Tests UnitSerializer for correct serialization, now expecting 'id'.
        """
        unittype = test_unit_type
        user = test_user
        unit = baker.make(Unit, name='Second', unit_type=unittype, user_id=user)

        serializer = UnitSerializer(instance=unit)
        expected_data = {
            'id': unit.id, # 'id' IS NOW included for UnitSerializer
            'name': 'Second',
            'unit_type': unittype.id, # unit_type is serialized as ID
        }
        assert serializer.data == expected_data
        assert 'id' in serializer.data # Explicitly check that 'id' IS present

    def test_unit_serializer_read_only_fields(self, test_unit_type, test_user): # Uses global fixtures
        """
        Tests that UnitSerializer fields ('name', 'unit_type') are read-only.
        """
        unittype = test_unit_type 
        user = test_user 
        unit = baker.make(Unit, name='Meter', unit_type=unittype, user_id=user)

        # Attempt to modify read-only fields (no 'id' in data for this serializer)
        data = {'name': 'Foot', 'unit_type': baker.make(UnitType, name='FootType').id} 
        serializer = UnitSerializer(instance=unit, data=data, partial=True)
        
        assert serializer.is_valid(raise_exception=True)
        updated_unit = serializer.save()
        
        # Ensure read-only fields are not updated
        assert updated_unit.name == unit.name # Name should not change
        assert updated_unit.unit_type == unit.unit_type # Unit type should not change

    def test_unit_admin_serializer_serialization(self, test_unit): # Uses global fixture
        """
        Tests UnitAdminSerializer for correct read-only serialization of all fields.
        """
        unit = test_unit
        # For comparison with created_at, ensure it's a datetime object
        unit.created_at = timezone.now()
        unit.save() # Save to update created_at for accurate comparison

        serializer = UnitAdminSerializer(instance=unit)
        
        assert 'id' in serializer.data
        assert 'name' in serializer.data
        assert 'unit_type' in serializer.data
        assert 'user_id' in serializer.data
        assert 'created_at' in serializer.data
        
        assert serializer.data['id'] == unit.id
        assert serializer.data['name'] == unit.name
        assert serializer.data['unit_type'] == unit.unit_type.id
        assert serializer.data['user_id'] == unit.user_id.id
        # Compare up to seconds for datetime accuracy
        assert serializer.data['created_at'].startswith(unit.created_at.isoformat().replace('+00:00', 'Z')[:19]) 


    def test_unit_admin_serializer_is_fully_read_only(self, test_user): # No need for test_unit_type fixture here
        """
        Tests that UnitAdminSerializer rejects any write attempts (create or update).
        """
        # Use a fresh Unit and UnitType for the update scenario
        unittype_for_update = baker.make(UnitType, name='OrgUTypeForU') 
        unit_instance_for_update = baker.make(Unit, name='OrgUnitU', unit_type=unittype_for_update, user_id=test_user)
        
        # Scenario 1: Attempt to update an existing Unit
        data_update = {
            'name': 'Updt UnitU', 
            'unit_type': baker.make(UnitType, name='NewUTypeForU').id, 
            'user_id': baker.make(CustomUser, username="new_user_for_u").id 
        }
        serializer_update = UnitAdminSerializer(instance=unit_instance_for_update, data=data_update, partial=True)
        
        assert serializer_update.is_valid(raise_exception=True) 
        with pytest.raises(ValidationError) as excinfo:
            serializer_update.save()
        assert "This serializer is read-only; updates are not allowed." in excinfo.value.detail[0]

        # Ensure no change to the original object
        unit_instance_for_update.refresh_from_db()
        assert unit_instance_for_update.name == 'OrgUnitU'


        # Scenario 2: Attempt to create a new Unit
        data_create = {
            'name': 'New Unt AtmptU', 
            'unit_type': baker.make(UnitType, name='AnoUTypeForU').id, 
            'user_id': baker.make(CustomUser, username="ano_user_for_u").id 
        }
        serializer_create = UnitAdminSerializer(data=data_create)
        
        assert serializer_create.is_valid(raise_exception=True)
        with pytest.raises(ValidationError) as excinfo:
            serializer_create.save()
        assert "This serializer is read-only; creation is not allowed." in excinfo.value.detail[0]

        # No new object should be created
        assert not Unit.objects.filter(name='New Unt AtmptU').exists()
