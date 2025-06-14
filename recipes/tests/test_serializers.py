import pytest
from rest_framework.exceptions import ValidationError
from model_bakery import baker
from django.utils import timezone 

# Import models - now many can be provided via global fixtures
from recipes.models.category import Category
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.step import Step
from users.models.user import CustomUser # Explicit import for CustomUser
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType
from media.models.image import Image 

# Import serializers
from recipes.serializers.categorySerializer import CategorySerializer, CategoryAdminSerializer
from recipes.serializers.ingredientSerializer import IngredientSerializer, IngredientAdminSerializer
from recipes.serializers.recipeIngredientSerializer import RecipeIngredientSerializer, RecipeIngredientAdminSerializer
from recipes.serializers.recipeSerializer import RecipeSerializer, RecipeAdminSerializer
from recipes.serializers.stepSerializer import StepSerializer, StepAdminSerializer
from users.serializers.userSerializer import CustomUserFrontSerializer
from media.serializers.image_serializer import ImageListSerializer


# --- Test Category Serializers ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.recipes_app
class TestCategorySerializers:

    @pytest.fixture
    def setup_category_data(self, test_user, test_category): # Uses test_user and test_category
        parent_cat = test_category # Use the fixture as parent
        # Create a new child category explicitly for this scenario
        category = baker.make(Category, name='ChildCat', user_id=test_user, parent_category_id=parent_cat)
        
        # Create related recipes and ingredients for this specific scenario
        recipe1 = baker.make(Recipe, name='Recipe Cat 1', user_id=test_user, duration_minutes=30, commensals=2)
        recipe2 = baker.make(Recipe, name='Recipe Cat 2', user_id=test_user, duration_minutes=40, commensals=4)
        category.recipes.add(recipe1, recipe2)
        
        unit_type_mass = baker.make(UnitType, name='MassUT') # Create specific unit type for ingredients
        ingredient1 = baker.make(Ingredient, name='Ingred Cat 1', user_id=test_user, unit_type_id=unit_type_mass)
        ingredient2 = baker.make(Ingredient, name='Ingred Cat 2', user_id=test_user, unit_type_id=unit_type_mass)
        category.ingredients.add(ingredient1, ingredient2)
        
        return {
            'category': category,
            'parent_cat': parent_cat,
            'user': test_user,
            'recipes': [recipe1, recipe2],
            'ingredients': [ingredient1, ingredient2],
            'unit_type_mass': unit_type_mass # Pass for later use if needed
        }

    def test_category_serializer_serialization(self, setup_category_data):
        """Tests CategorySerializer for correct serialization."""
        serializer = CategorySerializer(instance=setup_category_data['category'])
        data = serializer.data

        assert data['id'] == setup_category_data['category'].id
        assert data['name'] == 'ChildCat'
        assert data['user_id'] == setup_category_data['user'].id
        assert data['parent_category_id'] == setup_category_data['parent_cat'].id
        assert len(data['recipes']) == 2
        assert sorted([r['name'] for r in data['recipes']]) == sorted([r.name for r in setup_category_data['recipes']])
        assert len(data['ingredients']) == 2
        assert sorted([i['name'] for i in data['ingredients']]) == sorted([i.name for i in setup_category_data['ingredients']])

        # Check read_only_fields (no modifications should be possible via this serializer)
        assert serializer.fields['id'].read_only
        assert serializer.fields['name'].read_only
        assert serializer.fields['user_id'].read_only
        assert serializer.fields['parent_category_id'].read_only
        assert serializer.fields['recipes'].read_only
        assert serializer.fields['ingredients'].read_only

        # Attempt to update should not modify fields as per read_only_fields
        update_data = {'name': 'Updated Cat Name'}
        serializer_update = CategorySerializer(instance=setup_category_data['category'], data=update_data, partial=True)
        assert serializer_update.is_valid(raise_exception=True)
        updated_instance = serializer_update.save()
        assert updated_instance.name == setup_category_data['category'].name


    def test_category_admin_serializer_serialization(self, setup_category_data):
        """Tests CategoryAdminSerializer for correct serialization of all fields."""
        serializer = CategoryAdminSerializer(instance=setup_category_data['category'])
        data = serializer.data

        assert data['id'] == setup_category_data['category'].id
        assert data['name'] == 'ChildCat'
        assert data['user_id'] == setup_category_data['user'].id
        assert data['parent_category_id'] == setup_category_data['parent_cat'].id
        assert 'created_at' in data
        assert len(data['recipes']) == 2
        assert len(data['ingredients']) == 2

    def test_category_admin_serializer_update(self, setup_category_data, another_custom_user):
        """Tests that CategoryAdminSerializer can update fields (except read_only_fields)."""
        category_instance = setup_category_data['category']
        new_parent = baker.make(Category, name='NewParent', user_id=another_custom_user)
        
        data_update = {
            'name': 'UpdatedChildCat',
            'user_id': another_custom_user.id,
            'parent_category_id': new_parent.id
        }
        
        serializer_update = CategoryAdminSerializer(instance=category_instance, data=data_update, partial=True)
        assert serializer_update.is_valid(raise_exception=True)
        updated_category = serializer_update.save()

        assert updated_category.name == 'UpdatedChildCat'
        assert updated_category.user_id == another_custom_user
        assert updated_category.parent_category_id == new_parent
        assert updated_category.id == category_instance.id
        assert updated_category.created_at == category_instance.created_at

    def test_category_admin_serializer_create(self, test_user, another_custom_user, test_category): # Uses test_category
        """Tests that CategoryAdminSerializer can create new categories."""
        parent_cat = test_category # Use the fixture
        data_create = {
            'name': 'NewAdminCat',
            'user_id': another_custom_user.id,
            'parent_category_id': parent_cat.id
        }
        
        serializer_create = CategoryAdminSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        created_category = serializer_create.save()

        assert created_category.id is not None
        assert created_category.name == 'NewAdminCat'
        assert created_category.user_id == another_custom_user
        assert created_category.parent_category_id == parent_cat
        assert created_category.created_at is not None
        assert Category.objects.filter(name='NewAdminCat').exists()


# --- Test Ingredient Serializers ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.recipes_app
class TestIngredientSerializers:

    @pytest.fixture
    def setup_ingredient_serializer_data(self, test_user, test_unit_type): # Uses global fixtures
        # CORRECTED: Explicitly create ingredient with the name expected by tests
        ingredient = baker.make(Ingredient, name='MyIngredient', user_id=test_user, unit_type_id=test_unit_type, is_approved=False)
        category1 = baker.make(Category, name='CategoryA', user_id=test_user)
        category2 = baker.make(Category, name='CategoryB', user_id=test_user)
        ingredient.categories.add(category1, category2)
        return {
            'ingredient': ingredient,
            'user': test_user,
            'unit_type': test_unit_type,
            'categories': [category1, category2]
        }

    def test_ingredient_serializer_serialization(self, setup_ingredient_serializer_data):
        """Tests IngredientSerializer for correct serialization."""
        serializer = IngredientSerializer(instance=setup_ingredient_serializer_data['ingredient'])
        data = serializer.data

        assert data['id'] == setup_ingredient_serializer_data['ingredient'].id
        assert data['name'] == 'MyIngredient'
        assert data['user_id'] == setup_ingredient_serializer_data['user'].id
        assert data['unit_type_id'] == setup_ingredient_serializer_data['unit_type'].id
        assert data['is_approved'] is False
        assert data['categories'] == [cat.id for cat in setup_ingredient_serializer_data['categories']]
        assert 'created_at' in data
        assert 'updated_at' in data

        # Check read-only fields
        assert serializer.fields['id'].read_only
        assert serializer.fields['created_at'].read_only
        assert serializer.fields['updated_at'].read_only

        # Test update attempt on read-only fields
        update_data = {'id': 999, 'name': 'UpdatedName', 'created_at': timezone.now().isoformat()}
        serializer_update = IngredientSerializer(instance=setup_ingredient_serializer_data['ingredient'], data=update_data, partial=True)
        assert serializer_update.is_valid(raise_exception=True)
        updated_instance = serializer_update.save()
        assert updated_instance.id == setup_ingredient_serializer_data['ingredient'].id
        assert updated_instance.created_at == setup_ingredient_serializer_data['ingredient'].created_at
        assert updated_instance.updated_at == setup_ingredient_serializer_data['ingredient'].updated_at
        assert updated_instance.name == 'UpdatedName' # name should be writable by this serializer

    def test_ingredient_serializer_create(self, test_user, test_unit_type): # Uses global fixtures
        """Tests IngredientSerializer can create a new ingredient."""
        category = baker.make(Category, name='Dairy', user_id=test_user)
        data_create = {
            'name': 'Milk',
            'user_id': test_user.id,
            'unit_type_id': test_unit_type.id, # Use global fixture
            'is_approved': True,
            'categories': [category.id]
        }
        serializer_create = IngredientSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        created_ingredient = serializer_create.save()

        assert created_ingredient.id is not None
        assert created_ingredient.name == 'Milk'
        assert created_ingredient.user_id == test_user
        assert created_ingredient.unit_type_id == test_unit_type
        assert created_ingredient.is_approved is True
        assert created_ingredient.categories.count() == 1
        assert category in created_ingredient.categories.all()


    def test_ingredient_admin_serializer_serialization(self, setup_ingredient_serializer_data):
        """Tests IngredientAdminSerializer for correct serialization of all fields."""
        serializer = IngredientAdminSerializer(instance=setup_ingredient_serializer_data['ingredient'])
        data = serializer.data

        assert data['id'] == setup_ingredient_serializer_data['ingredient'].id
        assert data['name'] == 'MyIngredient'
        assert data['user_id'] == setup_ingredient_serializer_data['user'].id
        assert data['unit_type_id'] == setup_ingredient_serializer_data['unit_type'].id
        assert data['is_approved'] is False
        assert data['categories'] == [cat.id for cat in setup_ingredient_serializer_data['categories']]
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_ingredient_admin_serializer_update(self, setup_ingredient_serializer_data, another_custom_user, test_unit_type): # Uses global fixture
        """Tests that IngredientAdminSerializer can update fields (except read_only_fields)."""
        ingredient_instance = setup_ingredient_serializer_data['ingredient']
        new_unit_type = test_unit_type # Use global fixture or make a new one if different properties needed
        new_category = baker.make(Category, name='NewCategory', user_id=another_custom_user)

        data_update = {
            'name': 'UpdatedIngredient',
            'user_id': another_custom_user.id,
            'unit_type_id': new_unit_type.id,
            'is_approved': True,
            'categories': [new_category.id]
        }
        
        serializer_update = IngredientAdminSerializer(instance=ingredient_instance, data=data_update, partial=True)
        assert serializer_update.is_valid(raise_exception=True)
        updated_ingredient = serializer_update.save()

        assert updated_ingredient.name == 'UpdatedIngredient'
        assert updated_ingredient.user_id == another_custom_user
        assert updated_ingredient.unit_type_id == new_unit_type
        assert updated_ingredient.is_approved is True
        assert updated_ingredient.categories.count() == 1
        assert new_category in updated_ingredient.categories.all()

        assert updated_ingredient.id == ingredient_instance.id 
        assert updated_ingredient.created_at == ingredient_instance.created_at

    def test_ingredient_admin_serializer_create(self, test_user, test_unit_type): # Uses global fixtures
        """Tests IngredientAdminSerializer can create a new ingredient."""
        category = baker.make(Category, name='AdminCat', user_id=test_user)
        data_create = {
            'name': 'AdminMilk',
            'user_id': test_user.id,
            'unit_type_id': test_unit_type.id, # Use global fixture
            'is_approved': True,
            'categories': [category.id]
        }
        serializer_create = IngredientAdminSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        created_ingredient = serializer_create.save()

        assert created_ingredient.id is not None
        assert created_ingredient.name == 'AdminMilk'
        assert created_ingredient.user_id == test_user
        assert created_ingredient.unit_type_id == test_unit_type
        assert created_ingredient.is_approved is True
        assert created_ingredient.categories.count() == 1
        assert category in created_ingredient.categories.all()


# --- Test RecipeIngredient Serializers ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.recipes_app
class TestRecipeIngredientSerializers:

    @pytest.fixture
    def setup_recipe_ingredient_serializer_data(self, test_user, test_recipe, test_ingredient, test_unit, test_unit_type): # Uses global fixtures
        ri_instance = baker.make(RecipeIngredient, recipe=test_recipe, ingredient=test_ingredient, quantity=250, unit=test_unit)
        return {
            'recipe_ingredient': ri_instance,
            'recipe': test_recipe,
            'ingredient': test_ingredient,
            'unit': test_unit,
            'user': test_user,
            'unit_type': test_unit_type # For creating new ingredients if needed
        }

    def test_recipe_ingredient_serializer_serialization(self, setup_recipe_ingredient_serializer_data):
        """Tests RecipeIngredientSerializer for correct serialization."""
        serializer = RecipeIngredientSerializer(instance=setup_recipe_ingredient_serializer_data['recipe_ingredient'])
        data = serializer.data

        assert data['id'] == setup_recipe_ingredient_serializer_data['recipe_ingredient'].id
        assert data['recipe'] == setup_recipe_ingredient_serializer_data['recipe'].id
        assert data['quantity'] == 250
        assert data['ingredient'] == setup_recipe_ingredient_serializer_data['ingredient'].id
        assert data['unit'] == setup_recipe_ingredient_serializer_data['unit'].id


    def test_recipe_ingredient_serializer_create(self, test_user, test_recipe, test_ingredient, test_unit, test_unit_type): # Uses global fixtures
        """Tests RecipeIngredientSerializer can create a new RecipeIngredient."""
        # Use existing fixtures for related objects or create new ones for specific test scenarios
        new_recipe = baker.make(Recipe, name='New RI Recipe', user_id=test_user, duration_minutes=10, commensals=1)
        new_quantity = 500
        new_ingredient = baker.make(Ingredient, name='New Ingred for RI', user_id=test_user, unit_type_id=test_unit_type)
        new_unit = baker.make(Unit, name='NewUnit for RI', user_id=test_user, unit_type=test_unit_type)

        data_create = {
            'recipe': new_recipe.id,
            'quantity': new_quantity,
            'ingredient': new_ingredient.id,
            'unit': new_unit.id              
        }
        
        serializer_create = RecipeIngredientSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        created_ri = serializer_create.save()

        assert created_ri.id is not None
        assert created_ri.recipe == new_recipe
        assert created_ri.ingredient == new_ingredient
        assert created_ri.quantity == new_quantity
        assert created_ri.unit == new_unit


    def test_recipe_ingredient_admin_serializer_serialization(self, setup_recipe_ingredient_serializer_data):
        """Tests RecipeIngredientAdminSerializer for correct serialization."""
        serializer = RecipeIngredientAdminSerializer(instance=setup_recipe_ingredient_serializer_data['recipe_ingredient'])
        data = serializer.data

        assert data['id'] == setup_recipe_ingredient_serializer_data['recipe_ingredient'].id
        assert data['recipe'] == setup_recipe_ingredient_serializer_data['recipe'].id
        assert data['ingredient'] == setup_recipe_ingredient_serializer_data['ingredient'].id
        assert data['quantity'] == 250
        assert data['unit'] == setup_recipe_ingredient_serializer_data['unit'].id
        assert 'created_at' in data

    def test_recipe_ingredient_admin_serializer_update(self, setup_recipe_ingredient_serializer_data, test_user, test_unit_type): # Uses global fixtures
        """Tests RecipeIngredientAdminSerializer can update fields (except read_only_fields)."""
        ri_instance = setup_recipe_ingredient_serializer_data['recipe_ingredient']
        new_quantity = 300
        new_unit = baker.make(Unit, name='grams-upd', user_id=test_user, unit_type=test_unit_type)

        data_update = {
            'quantity': new_quantity,
            'unit': new_unit.id
        }
        serializer_update = RecipeIngredientAdminSerializer(instance=ri_instance, data=data_update, partial=True)
        assert serializer_update.is_valid(raise_exception=True)
        updated_ri = serializer_update.save()

        assert updated_ri.quantity == new_quantity
        assert updated_ri.unit == new_unit
        
        assert updated_ri.id == ri_instance.id
        assert updated_ri.created_at == ri_instance.created_at
        assert updated_ri.recipe == ri_instance.recipe
        assert updated_ri.ingredient == ri_instance.ingredient

    def test_recipe_ingredient_admin_serializer_create(self, test_user, test_recipe, test_ingredient, test_unit, test_unit_type): # Uses global fixtures
        """Tests RecipeIngredientAdminSerializer can create a new RecipeIngredient."""
        recipe = baker.make(Recipe, name='Admin RI Recipe', user_id=test_user, duration_minutes=15, commensals=1)
        unit_type = test_unit_type
        ingredient = baker.make(Ingredient, name='Admin Ingred RI', user_id=test_user, unit_type_id=unit_type)
        unit = baker.make(Unit, name='mlAdminRI', user_id=test_user, unit_type=unit_type)

        data_create = {
            'recipe': recipe.id,
            'ingredient': ingredient.id,
            'quantity': 75,
            'unit': unit.id
        }
        serializer_create = RecipeIngredientAdminSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        created_ri = serializer_create.save()

        assert created_ri.id is not None
        assert created_ri.recipe == recipe
        assert created_ri.ingredient == ingredient
        assert created_ri.quantity == 75
        assert created_ri.unit == unit
        assert RecipeIngredient.objects.filter(id=created_ri.id).exists()


# --- Test Recipe Serializers ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.serializers
@pytest.mark.recipes_app
class TestRecipeSerializers:

    @pytest.fixture
    def setup_recipe_serializer_data(self, test_user, test_unit_type): # Uses global fixtures
        # CORRECTED: Explicitly create recipe with the name expected by tests
        recipe = baker.make(Recipe, name='Test Recipe S', user_id=test_user, duration_minutes=30, commensals=2)
        category1 = baker.make(Category, name='CatRS1', user_id=test_user)
        category2 = baker.make(Category, name='CatRS2', user_id=test_user)
        recipe.categories.add(category1, category2)

        # Related ingredients and steps
        ingredient1 = baker.make(Ingredient, name='IngredRS1', user_id=test_user, unit_type_id=test_unit_type)
        ingredient2 = baker.make(Ingredient, name='IngredRS2', user_id=test_user, unit_type_id=test_unit_type)
        unit_g = baker.make(Unit, name='gRSI', user_id=test_user, unit_type=test_unit_type)
        
        ri1 = baker.make(RecipeIngredient, recipe=recipe, ingredient=ingredient1, quantity=100, unit=unit_g)
        ri2 = baker.make(RecipeIngredient, recipe=recipe, ingredient=ingredient2, quantity=200, unit=unit_g)
        
        step1 = baker.make(Step, recipe=recipe, order=1, description='Step 1 Desc')
        step2 = baker.make(Step, recipe=recipe, order=2, description='Step 2 Desc')
        
        image = baker.make(Image, external_id=recipe.id, type='RECIPE', url='http://example.com/test_recipe_image.jpg')

        return {
            'recipe': recipe,
            'user': test_user,
            'categories': [category1, category2],
            'ingredients': [ri1, ri2],
            'steps': [step1, step2],
            'image_instance': image
        }

    def test_recipe_serializer_serialization(self, setup_recipe_serializer_data):
        """Tests RecipeSerializer for correct serialization."""
        serializer = RecipeSerializer(instance=setup_recipe_serializer_data['recipe'])
        data = serializer.data

        assert data['id'] == setup_recipe_serializer_data['recipe'].id
        assert data['name'] == 'Test Recipe S'
        assert data['description'] == setup_recipe_serializer_data['recipe'].description
        assert data['user']['id'] == setup_recipe_serializer_data['user'].id
        assert data['user']['username'] == setup_recipe_serializer_data['user'].username
        assert data['duration_minutes'] == 30
        assert data['commensals'] == 2
        assert sorted(data['categories']) == sorted([cat.id for cat in setup_recipe_serializer_data['categories']])
        assert 'updated_at' in data
        assert 'image' in data 
        assert data['image']['url'] == 'http://example.com/test_recipe_image.jpg'


        assert len(data['ingredients']) == 2
        ri_names = [ri['ingredient'] for ri in data['ingredients']] 
        assert sorted(ri_names) == sorted([ing.id for ing in [ri.ingredient for ri in setup_recipe_serializer_data['ingredients']]])

        assert len(data['steps']) == 2
        step_descs = [s['description'] for s in data['steps']]
        assert sorted(step_descs) == sorted(['Step 1 Desc', 'Step 2 Desc'])

        assert serializer.fields['id'].read_only
        assert serializer.fields['user'].read_only
        assert serializer.fields['updated_at'].read_only

        update_data = {'id': 999, 'user': {'id': 100}, 'updated_at': timezone.now().isoformat()}
        serializer_update = RecipeSerializer(instance=setup_recipe_serializer_data['recipe'], data=update_data, partial=True)
        assert serializer_update.is_valid(raise_exception=True)
        updated_recipe = serializer_update.save()
        assert updated_recipe.id == setup_recipe_serializer_data['recipe'].id
        assert updated_recipe.user_id == setup_recipe_serializer_data['user']
        assert updated_recipe.updated_at == setup_recipe_serializer_data['recipe'].updated_at
        
        update_data = {'name': 'Updated Recipe Name'}
        serializer_update = RecipeSerializer(instance=setup_recipe_serializer_data['recipe'], data=update_data, partial=True)
        assert serializer_update.is_valid(raise_exception=True)
        updated_recipe = serializer_update.save()
        assert updated_recipe.name == 'Updated Recipe Name'


    def test_recipe_serializer_create(self, test_user, test_category): # Uses global fixture
        """Tests RecipeSerializer can create a new recipe."""
        category = test_category # Use the fixture
        data_create = {
            'name': 'New Recipe From Ser',
            'description': 'A fresh recipe.',
            'duration_minutes': 20,
            'commensals': 3,
            'categories': [category.id]
        }
        
        serializer_create = RecipeSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        created_recipe = serializer_create.save(user_id=test_user)

        assert created_recipe.id is not None
        assert created_recipe.name == 'New Recipe From Ser'
        assert created_recipe.user_id == test_user
        assert created_recipe.categories.count() == 1
        assert category in created_recipe.categories.all()


    def test_recipe_admin_serializer_serialization(self, setup_recipe_serializer_data):
        """Tests RecipeAdminSerializer for correct serialization."""
        serializer = RecipeAdminSerializer(instance=setup_recipe_serializer_data['recipe'])
        data = serializer.data

        assert data['id'] == setup_recipe_serializer_data['recipe'].id
        assert data['name'] == 'Test Recipe S'
        assert data['description'] == setup_recipe_serializer_data['recipe'].description
        assert data['user']['id'] == setup_recipe_serializer_data['user'].id
        assert data['user']['username'] == setup_recipe_serializer_data['user'].username
        assert data['duration_minutes'] == 30
        assert data['commensals'] == 2
        assert sorted(data['categories']) == sorted([cat.id for cat in setup_recipe_serializer_data['categories']])
        assert 'created_at' in data
        assert 'updated_at' in data
        assert 'image' in data 
        assert data['image'] == 'http://example.com/test_recipe_image.jpg'


        assert len(data['ingredients']) == 2
        ri_names = [ri['ingredient'] for ri in data['ingredients']] 
        assert sorted(ri_names) == sorted([ing.id for ing in [ri.ingredient for ri in setup_recipe_serializer_data['ingredients']]])

        assert len(data['steps']) == 2
        step_descs = [s['description'] for s in data['steps']]
        assert sorted(step_descs) == sorted(['Step 1 Desc', 'Step 2 Desc'])

        assert serializer.fields['id'].read_only
        assert serializer.fields['created_at'].read_only
        assert serializer.fields['updated_at'].read_only

    def test_recipe_admin_serializer_update(self, setup_recipe_serializer_data, another_custom_user, test_category): # Uses global fixture
        """Tests RecipeAdminSerializer can update fields (except read_only_fields)."""
        recipe_instance = setup_recipe_serializer_data['recipe']
        new_category = test_category # Use global fixture or make a new one if different properties needed
        
        data_update = {
            'name': 'Admin Updated Recipe',
            'description': 'Admin updated description',
            'duration_minutes': 60,
            'commensals': 6,
            'categories': [new_category.id]
        }
        
        serializer_update = RecipeAdminSerializer(instance=recipe_instance, data=data_update, partial=True)
        assert serializer_update.is_valid(raise_exception=True)
        updated_recipe = serializer_update.save()

        assert updated_recipe.name == 'Admin Updated Recipe'
        assert updated_recipe.description == 'Admin updated description'
        assert updated_recipe.duration_minutes == 60
        assert updated_recipe.commensals == 6
        assert updated_recipe.categories.count() == 1
        assert new_category in updated_recipe.categories.all()

        assert updated_recipe.id == recipe_instance.id
        assert updated_recipe.user_id == recipe_instance.user_id # Should be read-only if not provided in update
        assert updated_recipe.created_at == recipe_instance.created_at


    def test_recipe_admin_serializer_create(self, test_user, another_custom_user, test_category): # Uses global fixtures
        """Tests RecipeAdminSerializer can create a new recipe."""
        category = test_category # Use the fixture
        data_create = {
            'name': 'Admin New Recipe',
            'description': 'Admin created this.',
            'user_id': another_custom_user.id, # Admin can set user_id
            'duration_minutes': 25,
            'commensals': 4,
            'categories': [category.id]
        }
        
        serializer_create = RecipeAdminSerializer(data=data_create)
        assert serializer_create.is_valid(raise_exception=True)
        created_recipe = serializer_create.save()

        assert created_recipe.id is not None
        assert created_recipe.name == 'Admin New Recipe'
        assert created_recipe.user_id == another_custom_user
        assert created_recipe.categories.count() == 1
        assert category in created_recipe.categories.all()