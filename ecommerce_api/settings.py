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
db_name = os.getenv('DB_NAME', 'ecommerce_db')
db_host = os.getenv('DB_HOST')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
auth_source = os.getenv('AUTH_SOURCE', 'admin')

connect(
    host=db_host,
    username=db_username,
    password=db_password,
    authSource=auth_source
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