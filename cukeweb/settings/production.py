"""Production settings for cukeweb project."""

import os
import yaml
import psycopg2
from .base import *


ENV = yaml.load(open(os.environ['DJANGO_ENV_PATH']), Loader=yaml.FullLoader)

DEBUG = False
SECRET_KEY = ENV['SECRET_KEY']

ALLOWED_HOSTS += [
    '203.101.227.248',
    'cukes.neoformit.com',
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


ADMINS = [
    ("Cameron", "chyde1@usc.edu.au"),
    ("Cameron", "porkmymonkey@gmail.com"),
    # ("Peter", "pembleton@usc.edu.au"),
]
SERVER_EMAIL = 'admin@cukes.neoformit.com'
EMAIL_SUBJECT_PREFIX = '[Cukeweb Admin] '
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'admin'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'The Cuke Register <admin@cukes.neoformit.com>'


BASE_URL = 'https://cukes.neoformit.com/'
STATIC_ROOT = os.path.join(BASE_DIR, 'cukeweb', 'static')
