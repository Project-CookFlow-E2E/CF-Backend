import os
import dj_database_url
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-se*+7f6m+_anqy-ftqv$xuk^@+#1@n(-i+hziugch+=0oieb43'

DEBUG = True

ALLOWED_HOSTS = ['frontend', 'backend', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'api',
    'users',
    'recipes',
    'shopping',
    'measurements',
    'media',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"

]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

SIMPLE_JWT = {
    # ... tus otras configuraciones de SIMPLE_JWT

    'BLACKLIST_ENABLED': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5), # O el tiempo que tengas configurado
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # O el tiempo que tengas configurado
}

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'postgres://admin:admin@localhost:5432/cookflow_db'),
        conn_max_age=600)
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_IMAGE_MODEL = 'media.Image'
AUTH_RECIPE_MODEL = 'recipes.Recipe'
AUTH_CATEGORY_MODEL = 'recipes.Category'
AUTH_INGREDIENT_MODEL = 'recipes.Ingredient'
AUTH_RECIPEINGREDIENT_MODEL = 'recipes.RecipeIngredient'
AUTH_STEP_MODEL = 'recipes.Step'
AUTH_SHOPPINGLISTITEM_MODEL = 'shopping.ShoppingListItem'
AUTH_USER_MODEL = 'users.CustomUser'
AUTH_FAVORITE_MODEL = 'recipes.Favorite'
AUTH_UNIT_MODEL = 'measurements.Unit'
AUTH_UNITTYPE_MODEL = 'measurements.UnitType'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

ARGON2_DEFAULTS = {
    'time_cost': 4,
    'memory_cost': 4096,
    'parallelism': 2
}


MEDIA_IMG_PATH = BASE_DIR / 'media' / 'img'
# Media files configuration
MEDIA_URL = '/media/'  # URL accesible desde navegador (ej: http://localhost:8000/media/uuid.webp)
MEDIA_ROOT = BASE_DIR / 'media'  # Carpeta donde se guardan los archivos

# Carpeta específica para imágenes (usada en imageViewSet.py)
MEDIA_IMG_PATH = MEDIA_ROOT / 'img'

# API Documentación
SPECTACULAR_SETTINGS = {
    'TITLE': 'CookFlow API',
    'DESCRIPTION': 'API for managing recipes, users, and shopping lists.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False, # This makes sure the schema itself is not included in the UI by default
}