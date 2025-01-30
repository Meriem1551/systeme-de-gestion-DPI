"""
Django settings for TP_IGL project.

Generated by 'django-admin startproject' using Django 4.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!-4nj^&wxu%y+gvg#*j)t%svc-pj#rf(78xkvfg7ne4gz6mqg6"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",  # Ajoutez OPTIONS à la liste des méthodes autorisées
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]
# Application definition

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'gestiondpi',
    'authentification',
    'creationdpi',
    'miseajourdpi',
    'django_extensions',
    'rest_framework_swagger',
    'drf_yasg',
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "TP_IGL.urls"

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

WSGI_APPLICATION = "TP_IGL.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test1',
        'USER': 'root',
        'PASSWORD': 'enteresta',
=======
        'NAME': 'TP_IGL',
        'USER': 'fatma',
        'PASSWORD': '30 MAY 05 30 MAY 05',
        'HOST': 'localhost',
        'PORT': '3306',
=======  
        "NAME": "mydjango_db",
        "USER": "root",
        "PASSWORD": "mysql2024",
"""
DATABASES = {

    "default": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': 'battabase',
        'USER': 'root',
        'PASSWORD': 'batta2004',
        "HOST": "localhost",
        "PORT": "3306",

    }

}
'''
DATABASES['default']['TEST'] = {
    'NAME': 'test_igl_db',
}
'''

REST_FRAMEWORK={
    'NON_FIELD_ERRORS_KEY':'error',
        'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

    #'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',




# SPECTACULAR_SETTINGS = {
#     'TITLE': 'GesdtionDPI',  # The title of API
#     'DESCRIPTION': 'Detailed description of your API',  # Description of the API
#     'VERSION': '1.0.0',  # API version
#     'SERVE_INCLUDE_SCHEMA': False,  # This option is set to False if you do not want to expose the schema as an endpoint
# }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
AUTH_USER_MODEL = "authentification.User"

STATIC_URL = "static/"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
