"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from os import getenv as os_getenv
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os_getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os_getenv('ENV') == 'dev' else False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', ]
if os_getenv('EXTERNAL_URL'):
    ALLOWED_HOSTS.append(os_getenv('EXTERNAL_URL'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'thumbnails',
    'drf_spectacular',
    'django_celery_beat',
    'django_celery_results',
    'products',
    'orders',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
'ROTATE_REFRESH_TOKENS': False,
'BLACKLIST_AFTER_ROTATION': True,

'ALGORITHM': 'HS256',
'SIGNING_KEY': SECRET_KEY,
'VERIFYING_KEY': None,
'AUDIENCE': None,
'ISSUER': None,

'AUTH_HEADER_TYPES': ('Bearer',),
'USER_ID_FIELD': 'id',
'USER_ID_CLAIM': 'user_id',

'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
'TOKEN_TYPE_CLAIM': 'token_type',

'JTI_CLAIM': 'jti',
'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser'
}

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os_getenv('POSTGRES_DB'),
        'USER': os_getenv('POSTGRES_USER'),
        'PASSWORD': os_getenv('POSTGRES_PASS'),
        'HOST': os_getenv('POSTGRES_HOST'),
        'PORT': os_getenv('POSTGRES_PORT'), 
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# API Schema creation using drf-spectacular

SPECTACULAR_SETTINGS = {
    'TITLE': 'eCommerce DEMO API',
    'DESCRIPTION': 'REST API DEMO',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}


# Thumbnails generation - django-thumbnails

THUMBNAILS = {
    'METADATA': {
        'BACKEND': 'thumbnails.backends.metadata.DatabaseBackend',
    },
    'STORAGE': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'SIZES': {
        'small': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 200, 'height': 200, 'method':'fit'}
            ]
        }
    }
}


# Redis settings - need refactor as I opted for only-docker builds

REDIS_HOST = os_getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os_getenv('REDIS_PORT', 6379)

IS_DOCKER = os_getenv('IN_A_DOCKER_CONTAINER', False)
if IS_DOCKER:
    REDIS_HOST = 'redis'
    REDIS_PORT = 6379

REDIS_DB_KEYS = {
    'dev': 0,
    'test': 1,
    'prod': 2,
}

REDIS_DB = REDIS_DB_KEYS.get(os_getenv('ENV'))
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'


# Celery settings

CELERY_BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = {'application/json'}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'UTC'
CELERY_RESULT_EXTENDED = True

# Elasticsearch settings
ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'https://es01:9200',
        'http_auth': ('elastic', os_getenv('ELASTIC_PASSWORD'))
    }
}

# SMTP Settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = os_getenv('EMAIL_USE_TLS')
EMAIL_HOST = os_getenv('EMAIL_HOST')
EMAIL_HOST_USER = os_getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os_getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os_getenv('EMAIL_PORT')
EMAIL_DEFAULT_FROM = os_getenv('EMAIL_DEFAULT_FROM')


# Default users - created for dev environment

DEMO_SUPERUSER_PASS = 'admin123' # username admin
DEMO_MANAGER_PASS = 'manager123' # username manager
DEMO_CLIENT_PASS = 'client123'   # username client