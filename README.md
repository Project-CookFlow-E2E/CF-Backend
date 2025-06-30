# CookFlow Backend

CI 
This is the backend for the CookFlow project, powered by Django and PostgreSQL.

## Docker

Follow Instructions from Front End Repo 

## 🚀 Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the repository

`git clone https://github.com/Final-Project-CookFlow/CF-backend.git`
`cd CF-backend`

### 2. Create a virtual environment

`python -m venv venv`

3. Activate the virtual environment
   On macOS/Linux:
   `source venv/bin/activate`
   On Windows:
   `source venv/Scripts/activate`
   On Windows PowerShell:
   `.\venv\Scripts\Activate.ps1`

4. Install dependencies

`pip install -r requirements.txt`

### 3. 🛠️ Database Setup (PostgreSQL)

1. Create a new database.
   Create a new database named cookflow_db in your PostgreSQL.

2. Create a new role/user.
   Name: admin
   Password: admin
   Under Privileges, select all available options
   Save the new role

3. Run migrations.
   `python manage.py makemigrations`
   `python manage.py migrate`

## Alternative way Database Setup (PostgreSQL)

1. Access PostgreSQL as superuser (adjust psql command if needed).
   `psql -U postgres -h localhost`

2. Inside psql shell, run these commands (replace with your password if desired):

**PostgreSQL setup:**

```sql
CREATE USER admin WITH PASSWORD 'admin';
CREATE DATABASE cookflow_db OWNER admin;
GRANT ALL PRIVILEGES ON DATABASE cookflow_db TO admin;
\c cookflow_db;
GRANT USAGE ON SCHEMA public TO admin;
GRANT CREATE ON SCHEMA public TO admin;
\q
```

**PowerShell env variables:**

```powershell
$env:DJANGO_DB_USER="admin"
$env:DJANGO_DB_PASSWORD="admin"
$env:DJANGO_DB_NAME="cookflow_db"
$env:DJANGO_DB_HOST="localhost"
$env:DJANGO_DB_PORT="5432"
```

3. Run Django migrations

`python manage.py migrate`


# 🧪 Testing Overview
This section provides an overview of the unit tests implemented across different applications within the CookFlow backend. Our testing strategy ensures the reliability and correctness of both the data models and the serialization logic for various API endpoints.

All unit tests are run using pytest and are categorized using specific markers.

## Running Tests
To execute the unit tests, navigate to the root of your backend project and use the pytest command with the appropriate markers:
```
pytest -m "unit"
```
This command will execute all tests marked with "unit".

Application-Specific Tests
Here's a breakdown of the tests for each application:

### 👤 Users App (users)
Test Types: Model Tests, Serializer Tests

Coverage:

Model Tests (users/tests/test_models.py): Verify the CustomUser model's behavior, including default values, field validation, __str__ representation, and basic CRUD operations.

Serializer Tests (users/tests/test_serializers.py): Validate the CustomUserFrontSerializer and any admin-specific serializers for CustomUser, ensuring correct serialization, deserialization, creation, and update functionalities, along with proper handling of read-only fields.

### 📏 Measurements App (measurements)
Test Types: Model Tests, Serializer Tests

Coverage:

Model Tests (measurements/tests/test_models.py): Check the UnitType and Unit models for correct field definitions, relationships, __str__ representations, and cascading behaviors (e.g., when a UnitType is deleted).

Serializer Tests (measurements/tests/test_serializers.py): Confirm that UnitTypeSerializer, UnitTypeAdminSerializer, UnitSerializer, and UnitAdminSerializer correctly serialize and deserialize data, handle relationships, and enforce read-only constraints for different access levels.

### 🍽️ Recipes App (recipes)
Test Types: Model Tests, Serializer Tests

Coverage:

Model Tests (recipes/tests/test_models.py): Validate the core Category, Ingredient, Recipe, RecipeIngredient, and Step models. This includes testing field defaults, relationships (many-to-many, foreign keys), __str__ methods, and cascading deletions. Special attention is paid to how RecipeIngredient links recipes and ingredients.

Serializer Tests (recipes/tests/test_serializers.py): Ensure that CategorySerializer, CategoryAdminSerializer, IngredientSerializer, IngredientAdminSerializer, RecipeIngredientSerializer, RecipeIngredientAdminSerializer, RecipeSerializer, and RecipeAdminSerializer accurately handle data transformations. This involves checking correct serialization of nested data (like ingredients and steps within a recipe), handling of read-only fields, and proper creation/update flows for both standard and administrative interfaces.

### 🛒 Shopping App (shopping)
Test Types: Model Tests, Serializer Tests

Coverage:

Model Tests (shopping/tests/test_models.py): Focus on the ShoppingListItem model, verifying its fields, default values (e.g., is_purchased), relationships to users, ingredients, and units, and its string representation. Tests also cover cascade onDelete behavior for related objects.

Serializer Tests (shopping/tests/test_serializers.py): Validate ShoppingListItemSerializer (for standard users) and ShoppingListItemAdminSerializer (for administrators). These tests confirm accurate serialization, correct handling of creation and update operations (including ensuring read-only fields are not modified by unauthorized requests), and proper representation of related IDs.

CI Test 2
