from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-x(0xr90wv5^1d5%rfcpjjm=_(l1bf6zv#^(kgz5^+)&)sy+z7_'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_mongoengine',
    'core',  # Replace with the actual name of your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_api.wsgi.application'

# MongoDB Connection
from mongoengine import connect
connect(
    db='ecommerce_db',
    host='mongodb+srv://sakthivel19:Sakthivel-19@cluster0.yfwkf.mongodb.net/ecommerce_db?retryWrites=true&w=majority',
    username='sakthivel19',
    password='Sakthivel-19',
    authentication_source='admin'
)

SIMPLE_JWT = {
    'TOKEN_USER_CLASS': 'core.models.User',
    'USER_ID_FIELD': 'id',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authentication.MongoJWTAuthentication',
    ),
}

MIGRATION_MODULES = {
    'contenttypes': None,
    'sessions': None,
}

# Disable Django's auth system
AUTHENTICATION_BACKENDS = ['core.backends.MongoAuthBackend']

# Simple JWT config (will use our custom user model)
SIMPLE_JWT = {
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_USER_CLASS': 'core.models.User',
}

STATIC_URL = '/static/'