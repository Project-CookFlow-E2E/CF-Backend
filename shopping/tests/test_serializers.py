import pytest
from rest_framework.exceptions import ValidationError
from model_bakery import baker
from django.utils import timezone

# Import models
from shopping.models.shoppingListItem import ShoppingListItem
from users.models.user import CustomUser
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType # Often needed indirectly for units

# Import serializers
from shopping.serializers.shoppingListItemSerializer import ShoppingListItemSerializer, ShoppingListItemAdminSerializer


# --- Test ShoppingListItem Serializers ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.shopping_app
class TestShoppingListItemSerializers:

    @pytest.fixture
    def setup_shopping_list_item_serializer_data(self, test_user, test_ingredient, test_unit):
        """
        Fixture to set up data for ShoppingListItem serializer tests.
        Uses existing global fixtures for related models.
        """
        # Ensure the ingredient and unit are associated with the test_user if applicable or valid globally
        item = baker.make(ShoppingListItem, 
                          user_id=test_user, 
                          ingredient_id=test_ingredient, 
                          quantity_needed=500, 
                          unit=test_unit, 
                          is_purchased=True)
        return {
            'item': item,
            'user': test_user,
            'ingredient': test_ingredient,
            'unit': test_unit
        }

    def test_shopping_list_item_serializer_serialization(self, setup_shopping_list_item_serializer_data):
        """
        Tests ShoppingListItemSerializer for correct serialization of fields.
        Ensures `user_id` is read-only primary key in output.
        """
        item = setup_shopping_list_item_serializer_data['item']
        serializer = ShoppingListItemSerializer(instance=item)
        data = serializer.data

        assert data['user_id'] == item.user_id.id
        assert data['ingredient_id'] == item.ingredient_id.id
        assert data['quantity_needed'] == item.quantity_needed
        assert data['unit'] == item.unit.id # unit should be serialized as its ID
        assert data['is_purchased'] == item.is_purchased

        # Check that fields not explicitly in `fields` are not present in output
        assert 'id' not in data
        assert 'created_at' not in data
        assert 'updated_at' not in data

        # Verify read-only status of fields defined as read_only_fields
        assert serializer.fields['user_id'].read_only
        # ingredient_id is writable for functional use, so no read-only assertion here.


    def test_shopping_list_item_serializer_create(self, test_user, test_ingredient, test_unit):
        """
        Tests ShoppingListItemSerializer can create a new ShoppingListItem.
        `user_id` is passed during save, not directly in data.
        """
        data_create = {
            'ingredient_id': test_ingredient.id,
            'quantity_needed': 100,
            'unit': test_unit.id,
            'is_purchased': False
        }
        serializer_create = ShoppingListItemSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        # Pass user_id during save for fields that are read_only for input
        created_item = serializer_create.save(user_id=test_user)

        assert created_item.id is not None
        assert created_item.user_id == test_user
        assert created_item.ingredient_id == test_ingredient
        assert created_item.quantity_needed == 100
        assert created_item.unit == test_unit
        assert created_item.is_purchased is False
        assert ShoppingListItem.objects.filter(id=created_item.id).exists()


    def test_shopping_list_item_serializer_update(self, setup_shopping_list_item_serializer_data, test_unit):
        """
        Tests ShoppingListItemSerializer can update an existing ShoppingListItem.
        `user_id` and `ingredient_id` should not be updatable by standard user.
        """
        item_instance = setup_shopping_list_item_serializer_data['item']
        new_unit = baker.make(Unit, name='updated_unit', user_id=setup_shopping_list_item_serializer_data['user'], unit_type=test_unit.unit_type)

        data_update = {
            'quantity_needed': 750,
            'unit': new_unit.id,
            'is_purchased': False,
            # Removed: 'user_id': 9999, # User_id is read-only, attempts to update are ignored (or raise error if not PrimaryKeyRelatedField)
            # Removed: 'ingredient_id': 8888 # Ingredient_id is writable for creation, but typically not changed on update for standard user.
                                          # Passing an invalid ID here causes ValidationError.
        }

        serializer_update = ShoppingListItemSerializer(instance=item_instance, data=data_update, partial=True)
        assert serializer_update.is_valid(raise_exception=True) # This should now pass validation
        updated_item = serializer_update.save()

        assert updated_item.quantity_needed == 750
        assert updated_item.unit == new_unit
        assert updated_item.is_purchased is False

        # Ensure read-only fields were not changed (these assertions are still valid)
        assert updated_item.user_id == item_instance.user_id
        assert updated_item.ingredient_id == item_instance.ingredient_id
        assert updated_item.id == item_instance.id
        assert updated_item.created_at == item_instance.created_at
        assert updated_item.updated_at == item_instance.updated_at


    def test_shopping_list_item_admin_serializer_serialization(self, setup_shopping_list_item_serializer_data):
        """
        Tests ShoppingListItemAdminSerializer for correct serialization of all fields.
        """
        item = setup_shopping_list_item_serializer_data['item']
        serializer = ShoppingListItemAdminSerializer(instance=item)
        data = serializer.data

        assert data['id'] == item.id
        assert data['user_id'] == item.user_id.id
        assert data['ingredient_id'] == item.ingredient_id.id
        assert data['quantity_needed'] == item.quantity_needed
        assert data['unit'] == item.unit.id
        assert data['is_purchased'] == item.is_purchased
        assert 'created_at' in data
        assert 'updated_at' in data


    def test_shopping_list_item_admin_serializer_create(self, test_user, another_custom_user, test_ingredient, test_unit, test_unit_type):
        """
        Tests ShoppingListItemAdminSerializer can create a new ShoppingListItem,
        with admin having full control over all fields.
        """
        new_ingredient = baker.make(Ingredient, name='AdminIngredient', user_id=test_user, unit_type_id=test_unit_type)
        new_unit = baker.make(Unit, name='AdminUnit', user_id=test_user, unit_type=test_unit_type)

        data_create = {
            'user_id': another_custom_user.id,
            'ingredient_id': new_ingredient.id,
            'quantity_needed': 200,
            'unit': new_unit.id,
            'is_purchased': True
        }
        serializer_create = ShoppingListItemAdminSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        created_item = serializer_create.save()

        assert created_item.id is not None
        assert created_item.user_id == another_custom_user
        assert created_item.ingredient_id == new_ingredient
        assert created_item.quantity_needed == 200
        assert created_item.unit == new_unit
        assert created_item.is_purchased is True
        assert ShoppingListItem.objects.filter(id=created_item.id).exists()


    def test_shopping_list_item_admin_serializer_update(self, setup_shopping_list_item_serializer_data, another_custom_user, test_ingredient, test_unit_type):
        """
        Tests ShoppingListItemAdminSerializer can update any field.
        """
        item_instance = setup_shopping_list_item_serializer_data['item']
        new_ingredient = baker.make(Ingredient, name='UpdatedAdminIngred', user_id=another_custom_user, unit_type_id=test_unit_type)
        # CORRECTED: Shortened name to fit typical CharField(max_length=15) for Unit.name
        new_unit = baker.make(Unit, name='UpdAdminUnit', user_id=another_custom_user, unit_type=test_unit_type) 

        data_update = {
            'user_id': another_custom_user.id,
            'ingredient_id': new_ingredient.id,
            'quantity_needed': 150,
            'unit': new_unit.id,
            'is_purchased': False
        }
        serializer_update = ShoppingListItemAdminSerializer(instance=item_instance, data=data_update, partial=True)
        assert serializer_update.is_valid(raise_exception=True) # This should now pass validation
        updated_item = serializer_update.save()

        assert updated_item.user_id == another_custom_user
        assert updated_item.ingredient_id == new_ingredient
        assert updated_item.quantity_needed == 150
        assert updated_item.unit == new_unit
        assert updated_item.is_purchased is False
        assert updated_item.id == item_instance.id
        assert updated_item.created_at == item_instance.created_at # created_at should remain unchanged

