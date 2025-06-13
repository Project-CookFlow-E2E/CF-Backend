# measurements/tests/conftest.py
import pytest
from model_bakery import baker
from measurements.models import Unit, UnitType
from users.models.user import CustomUser

@pytest.fixture
def test_unittype(db):
    """
    Creates and returns a dummy UnitType instance.
    This can be used for tests that need a UnitType object.
    """
    return baker.make(UnitType, name='WeightType')

@pytest.fixture
def test_unit(db, test_unittype, test_user):
    """
    Creates and returns a dummy Unit instance.
    It automatically uses the test_unittype and test_user fixtures.
    """
    return baker.make(Unit, name='Kilogram', unit_type=test_unittype, user_id=test_user)

@pytest.fixture
def test_unittype_data():
    """
    Returns a dictionary of valid UnitType data for creation.
    """
    return {
        'name': 'LengthType',
    }

@pytest.fixture
def test_unit_data(test_unittype_data, test_user):
    """
    Returns a dictionary of valid Unit data for creation.
    Depends on test_unittype_data and test_user to provide related IDs.
    Note: For creation, you typically pass the ID of the foreign key, not the object.
    """
    unittype = baker.make(UnitType, **test_unittype_data)
    
    return {
        'name': 'Meter',
        'unit_type': unittype.id,
        'user_id': test_user.id, 
    }
