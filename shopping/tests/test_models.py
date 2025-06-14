import pytest
from model_bakery import baker
from django.utils import timezone
from django.db.utils import IntegrityError

# Import necessary models
from shopping.models.shoppingListItem import ShoppingListItem
from users.models.user import CustomUser # Assuming CustomUser is your AUTH_USER_MODEL
from recipes.models.ingredient import Ingredient
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType # Needed to create Unit instances


@pytest.mark.django_db
@pytest.mark.models
@pytest.mark.unit
@pytest.mark.shopping_app
class TestShoppingListItemModel:
    """
    Tests for the ShoppingListItem model.
    """

    @pytest.fixture
    def setup_shopping_list_item_data(self, test_user, test_ingredient, test_unit):
        """
        Fixture to set up common data for ShoppingListItem tests.
        Uses global fixtures: test_user, test_ingredient, test_unit.
        """
        user = test_user
        ingredient = test_ingredient
        unit = test_unit

        item = baker.make(
            ShoppingListItem,
            user_id=user,
            ingredient_id=ingredient,
            quantity_needed=10,
            unit=unit,
            is_purchased=False,
            created_at=timezone.now()
        )
        item.refresh_from_db() # IMPORTANT: Refresh the item from DB to ensure __str__ and relations are active
        return {
            'item': item,
            'user': user,
            'ingredient': ingredient,
            'unit': unit
        }

    def test_shopping_list_item_creation(self, setup_shopping_list_item_data):
        """
        Tests that a ShoppingListItem can be created successfully.
        """
        item = setup_shopping_list_item_data['item']
        
        assert item.id is not None
        assert item.user_id == setup_shopping_list_item_data['user']
        assert item.ingredient_id == setup_shopping_list_item_data['ingredient']
        assert item.quantity_needed == 10
        assert item.unit == setup_shopping_list_item_data['unit']
        assert item.is_purchased is False
        assert item.created_at is not None
        assert item.updated_at is not None
        assert item.created_at <= item.updated_at # created_at should be less than or equal to updated_at

    def test_shopping_list_item_defaults(self, test_user, test_ingredient, test_unit):
        """
        Tests default values for ShoppingListItem fields.
        Specifically, tests that `is_purchased` defaults to False.
        """
        item = baker.make(
            ShoppingListItem,
            user_id=test_user,
            ingredient_id=test_ingredient,
            quantity_needed=1,
            unit=test_unit
        )
        item.refresh_from_db() # Ensure __str__ and relations are active
        assert item.is_purchased is False

    def test_shopping_list_item_relationships(self, setup_shopping_list_item_data):
        """
        Tests that foreign key relationships are correctly established.
        """
        item = setup_shopping_list_item_data['item']
        user = setup_shopping_list_item_data['user']
        ingredient = setup_shopping_list_item_data['ingredient']
        unit = setup_shopping_list_item_data['unit']

        assert item.user_id.id == user.id
        assert item.ingredient_id.id == ingredient.id
        assert item.unit.id == unit.id

    def test_shopping_list_item_str_representation(self, setup_shopping_list_item_data):
        """
        Tests the __str__ method of the ShoppingListItem model.
        """
        item = setup_shopping_list_item_data['item']
        expected_str = f"{item.quantity_needed} {item.unit.name} of {item.ingredient_id.name} for {item.user_id.username}"
        assert str(item) == expected_str

    def test_shopping_list_item_update(self, setup_shopping_list_item_data):
        """
        Tests updating fields of an existing ShoppingListItem.
        """
        item = setup_shopping_list_item_data['item']
        old_updated_at = item.updated_at

        item.quantity_needed = 25
        item.is_purchased = True
        item.save()
        item.refresh_from_db() # Reload from DB to get updated values

        assert item.quantity_needed == 25
        assert item.is_purchased is True
        assert item.updated_at > old_updated_at # updated_at should have changed

    def test_shopping_list_item_deletion_cascades_from_user(self, db, test_ingredient, test_unit): # Removed setup_fixture, made independent
        """
        Tests that deleting a user cascades and deletes their shopping list items.
        This test creates its own isolated user and related objects.
        """
        # Create an isolated user for this specific deletion test
        user_to_delete = baker.make(CustomUser, username='user_for_delete_test')
        item_to_delete = baker.make(
            ShoppingListItem,
            user_id=user_to_delete,
            ingredient_id=test_ingredient, # Can reuse global ingredient/unit
            quantity_needed=10,
            unit=test_unit,
            is_purchased=False
        )

        assert ShoppingListItem.objects.filter(id=item_to_delete.id).exists()
        user_to_delete.delete()
        assert not ShoppingListItem.objects.filter(id=item_to_delete.id).exists()

    def test_shopping_list_item_deletion_cascades_from_ingredient(self, setup_shopping_list_item_data):
        """
        Tests that deleting an ingredient cascades and deletes associated shopping list items.
        """
        ingredient = setup_shopping_list_item_data['ingredient']
        item = setup_shopping_list_item_data['item']

        assert ShoppingListItem.objects.filter(id=item.id).exists()
        ingredient.delete()
        assert not ShoppingListItem.objects.filter(id=item.id).exists()

    def test_shopping_list_item_deletion_cascades_from_unit(self, setup_shopping_list_item_data):
        """
        Tests that deleting a unit cascades and deletes associated shopping list items.
        """
        unit = setup_shopping_list_item_data['unit']
        item = setup_shopping_list_item_data['item']

        assert ShoppingListItem.objects.filter(id=item.id).exists()
        unit.delete()
        assert not ShoppingListItem.objects.filter(id=item.id).exists()

    def test_shopping_list_item_constraints(self, test_user, test_ingredient, test_unit):
        """
        Tests any specific constraints (e.g., uniqueness) if applicable.
        For ShoppingListItem, multiple items for the same user/ingredient might be allowed,
        so no specific uniqueness test unless specified.
        This is a placeholder for future constraints.
        """
        # Example: if user_id, ingredient_id were unique_together
        # with pytest.raises(IntegrityError):
        #     baker.make(ShoppingListItem, user_id=test_user, ingredient_id=test_ingredient, quantity_needed=5, unit=test_unit)
        
        # For now, just test basic creation again
        item1 = baker.make(ShoppingListItem, user_id=test_user, ingredient_id=test_ingredient, quantity_needed=1, unit=test_unit)
        item2 = baker.make(ShoppingListItem, user_id=test_user, ingredient_id=test_ingredient, quantity_needed=2, unit=test_unit)
        assert item1.id != item2.id # Ensure two separate items can be created for same user/ingredient
