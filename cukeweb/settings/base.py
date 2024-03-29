"""Django settings for cukeweb project."""

import os
from .logconf import LOGGING


DEBUG = False
LOGGING['loggers']['django']['level'] = 'INFO'

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOGIN_URL = '/login'
LOGIN_REQUIRED_IGNORE_PATHS = [
    r'^/$',
]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'match',
    'manager',
    'register',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'login_required.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'cukeweb.urls'

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

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': ('django.contrib.auth.password_validation'
              '.UserAttributeSimilarityValidator')},
    {'NAME': ('django.contrib.auth.password_validation'
              '.MinimumLengthValidator')},
    {'NAME': ('django.contrib.auth.password_validation'
              '.CommonPasswordValidator')},
    {'NAME': ('django.contrib.auth.password_validation'
              '.NumericPasswordValidator')},
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Brisbane'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Root locations
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'cukeweb', 'media')

# File permissions (static/media) (breaks collectstatic!?)
# FILE_UPLOAD_PERMISSIONS = 0o644
# FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o644
