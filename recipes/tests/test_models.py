import pytest
from model_bakery import baker
from django.db.utils import IntegrityError, DataError

# Import models from recipes app
from recipes.models.category import Category
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe
from recipes.models.recipeIngredient import RecipeIngredient
from recipes.models.step import Step

# Import models from other apps that are ForeignKeys
from users.models.user import CustomUser
from measurements.models.unit import Unit
from measurements.models.unitType import UnitType


# --- Test Category Model ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.recipes_app
class TestCategoryModel:

    def test_category_creation(self, test_user):
        """Tests that a Category can be created successfully."""
        category = Category.objects.create(name='Desserts', user_id=test_user)
        assert category.id is not None
        assert category.name == 'Desserts'
        assert category.user_id == test_user
        assert category.parent_category_id is None
        assert Category.objects.count() == 1

    def test_category_unique_name(self, test_user):
        """Tests that category names are unique."""
        Category.objects.create(name='Main Dishes', user_id=test_user)
        with pytest.raises(IntegrityError):
            Category.objects.create(name='Main Dishes', user_id=test_user)

    def test_category_name_max_length(self, test_user):
        """Tests max_length for category name field."""
        long_name = 'a' * 51 # Max length is 50
        with pytest.raises(DataError):
            Category.objects.create(name=long_name, user_id=test_user)

    def test_category_str_representation(self, test_user):
        """Tests the __str__ method of Category model."""
        category = Category.objects.create(name='Soups', user_id=test_user)
        assert str(category) == 'Soups'

    def test_category_parent_category(self, test_user):
        """Tests creating a sub-category with a parent category."""
        parent = Category.objects.create(name='European', user_id=test_user)
        child = Category.objects.create(name='Italian', user_id=test_user, parent_category_id=parent)
        assert child.parent_category_id == parent
        assert Category.objects.count() == 2


# --- Test Ingredient Model ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.recipes_app
class TestIngredientModel:

    @pytest.fixture
    def setup_ingredient_data(self, test_user, test_unit_type): # Uses global fixtures
        return {
            'user': test_user,
            'unit_type': test_unit_type
        }

    def test_ingredient_creation(self, setup_ingredient_data):
        """Tests that an Ingredient can be created successfully."""
        ingredient = Ingredient.objects.create(
            name='Flour',
            user_id=setup_ingredient_data['user'],
            unit_type_id=setup_ingredient_data['unit_type'],
            is_approved=True
        )
        assert ingredient.id is not None
        assert ingredient.name == 'Flour'
        assert ingredient.user_id == setup_ingredient_data['user']
        assert ingredient.unit_type_id == setup_ingredient_data['unit_type']
        assert ingredient.is_approved is True
        assert Ingredient.objects.count() == 1

    def test_ingredient_unique_name(self, setup_ingredient_data):
        """Tests that ingredient names are unique."""
        Ingredient.objects.create(
            name='Salt',
            user_id=setup_ingredient_data['user'],
            unit_type_id=setup_ingredient_data['unit_type']
        )
        with pytest.raises(IntegrityError):
            Ingredient.objects.create(
                name='Salt',
                user_id=setup_ingredient_data['user'],
                unit_type_id=setup_ingredient_data['unit_type']
            )

    def test_ingredient_name_max_length(self, setup_ingredient_data):
        """Tests max_length for ingredient name field."""
        long_name = 'b' * 51 # Max length is 50
        with pytest.raises(DataError):
            Ingredient.objects.create(
                name=long_name,
                user_id=setup_ingredient_data['user'],
                unit_type_id=setup_ingredient_data['unit_type']
            )

    def test_ingredient_str_representation(self, setup_ingredient_data):
        """Tests the __str__ method of Ingredient model."""
        ingredient = Ingredient.objects.create(
            name='Sugar',
            user_id=setup_ingredient_data['user'],
            unit_type_id=setup_ingredient_data['unit_type']
        )
        assert str(ingredient) == 'Sugar'

    def test_ingredient_categories_relationship(self, setup_ingredient_data, test_user): # Uses test_user
        """Tests the ManyToMany relationship with Category."""
        category1 = baker.make(Category, name='Baking', user_id=test_user)
        category2 = baker.make(Category, name='Sweeteners', user_id=test_user)
        ingredient = Ingredient.objects.create(
            name='Vanilla',
            user_id=setup_ingredient_data['user'],
            unit_type_id=setup_ingredient_data['unit_type']
        )
        ingredient.categories.add(category1, category2)
        assert ingredient.categories.count() == 2
        assert category1 in ingredient.categories.all()
        assert category2 in ingredient.categories.all()
        assert ingredient in category1.ingredients.all()


# --- Test Recipe Model ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.recipes_app
class TestRecipeModel:

    @pytest.fixture
    def setup_recipe_data(self, test_user, test_category): # Uses global fixtures
        category1 = test_category
        category2 = baker.make(Category, name='AnotherCat', user_id=test_user) # Make another for scenario
        return {
            'user': test_user,
            'categories': [category1, category2]
        }

    def test_recipe_creation(self, setup_recipe_data):
        """Tests that a Recipe can be created successfully."""
        recipe = Recipe.objects.create(
            name='Chicken Stir-fry',
            description='Quick and healthy stir-fry',
            user_id=setup_recipe_data['user'],
            duration_minutes=25,
            commensals=2
        )
        recipe.categories.set(setup_recipe_data['categories']) # Set M2M after creation
        
        assert recipe.id is not None
        assert recipe.name == 'Chicken Stir-fry'
        assert recipe.user_id == setup_recipe_data['user']
        assert recipe.duration_minutes == 25
        assert recipe.commensals == 2
        assert recipe.categories.count() == 2
        assert Recipe.objects.count() == 1

    def test_recipe_name_max_length(self, test_user):
        """Tests max_length for recipe name field (50 characters)."""
        long_name = 'c' * 51
        with pytest.raises(DataError):
            Recipe.objects.create(
                name=long_name,
                user_id=test_user,
                duration_minutes=10,
                commensals=1
            )

    def test_recipe_description_null_blank(self, test_user):
        """Tests that description can be null and blank."""
        recipe = Recipe.objects.create(
            name='Simple Salad',
            description=None,
            user_id=test_user,
            duration_minutes=15,
            commensals=1
        )
        assert recipe.description is None
        recipe2 = Recipe.objects.create(
            name='Another Salad',
            description="",
            user_id=test_user,
            duration_minutes=15,
            commensals=1
        )
        assert recipe2.description == ""

    def test_recipe_str_representation(self, test_user):
        """Tests the __str__ method of Recipe model."""
        recipe = Recipe.objects.create(
            name='Smoothie',
            user_id=test_user,
            duration_minutes=5,
            commensals=1
        )
        assert str(recipe) == 'Smoothie'

    def test_recipe_categories_reverse_relationship(self, setup_recipe_data):
        """Tests the reverse ManyToMany relationship from Category to Recipe."""
        category = setup_recipe_data['categories'][0]
        recipe1 = baker.make(Recipe, name='Recipe A', user_id=setup_recipe_data['user'])
        recipe2 = baker.make(Recipe, name='Recipe B', user_id=setup_recipe_data['user'])
        
        recipe1.categories.add(category)
        recipe2.categories.add(category)

        assert category.recipes.count() == 2
        assert recipe1 in category.recipes.all()
        assert recipe2 in category.recipes.all()


# --- Test RecipeIngredient Model ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.recipes_app
class TestRecipeIngredientModel:

    @pytest.fixture
    def setup_recipe_ingredient_data(self, test_user, test_recipe, test_ingredient, test_unit_type, test_unit): # Uses global fixtures
        recipe = test_recipe
        ingredient = test_ingredient
        unit = test_unit
        
        return {
            'recipe': recipe,
            'ingredient': ingredient,
            'unit': unit,
            'user': test_user,
            'unit_type': test_unit_type # For creating new ingredients if needed
        }

    def test_recipe_ingredient_creation(self, setup_recipe_ingredient_data):
        """Tests that a RecipeIngredient can be created successfully."""
        ri = RecipeIngredient.objects.create(
            recipe=setup_recipe_ingredient_data['recipe'],
            ingredient=setup_recipe_ingredient_data['ingredient'],
            quantity=100,
            unit=setup_recipe_ingredient_data['unit']
        )
        assert ri.id is not None
        assert ri.recipe == setup_recipe_ingredient_data['recipe']
        assert ri.ingredient == setup_recipe_ingredient_data['ingredient']
        assert ri.quantity == 100
        assert ri.unit == setup_recipe_ingredient_data['unit']
        assert RecipeIngredient.objects.count() == 1

    def test_recipe_ingredient_str_representation(self, setup_recipe_ingredient_data):
        """Tests the __str__ method of RecipeIngredient model."""
        ri = RecipeIngredient.objects.create(
            recipe=setup_recipe_ingredient_data['recipe'],
            ingredient=setup_recipe_ingredient_data['ingredient'],
            quantity=5,
            unit=setup_recipe_ingredient_data['unit']
        )
        expected_str = f"5 {setup_recipe_ingredient_data['unit'].name} of {setup_recipe_ingredient_data['ingredient'].name} for {setup_recipe_ingredient_data['recipe'].name}"
        assert str(ri) == expected_str

    def test_recipe_ingredients_reverse_relationship(self, setup_recipe_ingredient_data, test_user, test_unit_type): # Uses global fixtures
        """Tests reverse relationship from Recipe to RecipeIngredient."""
        recipe = setup_recipe_ingredient_data['recipe']
        ingredient1 = baker.make(Ingredient, name='Ingred 1', user_id=test_user, unit_type_id=test_unit_type)
        ingredient2 = baker.make(Ingredient, name='Ingred 2', user_id=test_user, unit_type_id=test_unit_type)
        unit_ml = baker.make(Unit, name='ml', user_id=test_user, unit_type=test_unit_type)

        ri1 = RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1, quantity=10, unit=unit_ml)
        ri2 = RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2, quantity=20, unit=unit_ml)

        assert recipe.recipe_ingredients.count() == 2
        assert ri1 in recipe.recipe_ingredients.all()
        assert ri2 in recipe.recipe_ingredients.all()


# --- Test Step Model ---
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.recipes_app
class TestStepModel:

    @pytest.fixture
    def setup_step_data(self, test_user, test_recipe): # Uses global fixtures
        recipe = test_recipe
        return {
            'recipe': recipe,
            'user': test_user
        }

    def test_step_creation(self, setup_step_data):
        """Tests that a Step can be created successfully."""
        step = Step.objects.create(
            order=1,
            recipe=setup_step_data['recipe'],
            description='Chop vegetables'
        )
        assert step.id is not None
        assert step.order == 1
        assert step.recipe == setup_step_data['recipe']
        assert step.description == 'Chop vegetables'
        assert Step.objects.count() == 1

    def test_step_description_max_length(self, setup_step_data):
        """Tests max_length for step description field (100 characters)."""
        long_description = 'd' * 101
        with pytest.raises(DataError):
            Step.objects.create(
                order=1,
                recipe=setup_step_data['recipe'],
                description=long_description
            )

    def test_step_str_representation(self, setup_step_data):
        """Tests the __str__ method of Step model."""
        step = Step.objects.create(
            order=1,
            recipe=setup_step_data['recipe'],
            description='Preheat oven to 200C'
        )
        expected_str_prefix = f"Step 1 for {setup_step_data['recipe'].name}: Preheat oven to 200C..."
        assert str(step).startswith(expected_str_prefix[:30])

    def test_step_recipe_reverse_relationship(self, setup_step_data):
        """Tests reverse relationship from Recipe to Step."""
        recipe = setup_step_data['recipe']
        step1 = Step.objects.create(order=1, recipe=recipe, description='First step')
        step2 = Step.objects.create(order=2, recipe=recipe, description='Second step')

        assert recipe.step_set.count() == 2
        assert step1 in recipe.step_set.all()
        assert step2 in recipe.step_set.all()

