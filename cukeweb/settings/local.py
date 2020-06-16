"""Local settings for cukeweb project."""

import os
import yaml
import psycopg2
from .base import *


DEBUG = True
ENV = yaml.load(os.environ['ENV_PATH'], Loader=yaml.FullLoader)
SECRET_KEY = ENV['SECRET_KEY']
WSGI_APPLICATION = 'cukeweb.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cukeweb',
        'USER': 'cameron',
        'PASSWORD': ENV['DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'OPTIONS': {
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
    },
}


BASE_URL = 'http://127.0.0.1:8000/'
SERVER_EMAIL = 'admin@cukeregister.com'
