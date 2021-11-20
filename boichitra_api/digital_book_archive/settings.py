"""
Django settings for digital_book_archive project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from rest_framework.settings import api_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+wz2lp+$8)07r$$&7%+r&@6ly)6s4@19p2hjki!%*lr8*$_8)g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [

    # 'audiofield',

    'knox',
    'user_auth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    # user defined apps

    'user_profile',
    'archive',
    'subscription',
]
AUTH_USER_MODEL = 'user_auth.User'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'audiofield.middleware.threadlocals.ThreadLocals',
]


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'knox.auth.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}


REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
  # 'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'TOKEN_TTL': timedelta(hours=2160),  # default time 10h
  'USER_SERIALIZER': 'knox.serializers.UserSerializer',
  'TOKEN_LIMIT_PER_USER': None,
  'AUTO_REFRESH': False,
  # 'EXPIRY_DATETIME_FORMAT': api_settings.DATETME_FORMAT,
}

ROOT_URLCONF = 'digital_book_archive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'digital_book_archive.wsgi.application'


CORS_ORIGIN_ALLOW_ALL = True


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10000),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# AUTH_USER_MODEL = 'user_auth.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Email configuration for gmail
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'carlossde.hs@gmail.com'
EMAIL_HOST_PASSWORD = 'Saleh@12#$'
EMAIL_PORT = 587

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static", "static-only")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'static'), )

# Media Files

MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT  =   os.path.join(PROJECT_ROOT, 'media')


# Audiofield stuff

# Frontend widget values
# 0-Keep original, 1-Mono, 2-Stereo
CHANNEL_TYPE_VALUE = 0
# 0-Keep original, 8000-8000Hz, 16000-16000Hz, 22050-22050Hz,
# 44100-44100Hz, 48000-48000Hz, 96000-96000Hz
FREQ_TYPE_VALUE = 8000

# 0-Keep original, 1-Convert to MP3, 2-Convert to WAV, 3-Convert to OGG
CONVERT_TYPE_VALUE = 0

# Cors
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True