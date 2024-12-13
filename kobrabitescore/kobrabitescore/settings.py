import logging
import os
import sys
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-)&c5=b6m!0b61i-)_#s26pv*mxy&xsct3)0bmh509h(vby)q5k')

DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:57593').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:57593').split(',')

CORS_ALLOWED_ORIGINS.append('http://localhost:64473')
CSRF_TRUSTED_ORIGINS.append('http://localhost:64473')

CORS_ALLOWED_ORIGINS.append('https://kobrabites-backend-czh3g7fye3e5e2eg.canadacentral-01.azurewebsites.net')
CSRF_TRUSTED_ORIGINS.append('https://kobrabites-backend-czh3g7fye3e5e2eg.canadacentral-01.azurewebsites.net')


CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "SAMEORIGIN"

INSTALLED_APPS = [
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Party
    'corsheaders',
    'db_mutex',
    'django_filters',
    'drf_spectacular',
    'rest_framework',
    'storages',
    'django_bootstrap5',
    'django_celery_beat',
    'django_celery_results',
    'django.contrib.postgres',  # for full-text search features

    # Internal apps
    'api',
    'user',
    'client',
    'mealplanning',
    'social'
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'kobrabitescore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kobrabitescore.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'SET_ME_IN_LOCAL'),
        'USER': os.getenv('DB_USER', 'SET_ME_IN_LOCAL'),
        'PASSWORD': os.getenv('DB_PASS', 'SET_ME_IN_LOCAL'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'user.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'