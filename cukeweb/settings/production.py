"""Production settings for cukeweb project."""

import os
import yaml
import psycopg2
from .base import *


ENV = yaml.load(os.environ['ENV_PATH'], Loader=yaml.FullLoader)

DEBUG = False
SECRET_KEY = ENV['SECRET_KEY']

ALLOWED_HOSTS += [
    '203.101.227.248',
]

MIDDLEWARE += [
    # whitenoise
]


WSGI_APPLICATION = 'cukeweb.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ENV['DB_NAME'],
        'USER': ENV['DB_USER'],
        'PASSWORD': ENV['DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'OPTIONS': {
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
    },
}


# ADMINS = [            Need to configure these
#     ("Cameron", "chyde1@usc.edu.au"),
#     ("Cameron", "porkmymonkey@gmail.com"),
# ]
SERVER_EMAIL = 'admin@thecukeregister.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'admin'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'The Cuke Register <admin@crustybase.org>'


BASE_URL = 'hmmm...'
STATIC_ROOT = os.path.join(BASE_DIR, 'cukeweb', 'staticfiles')
