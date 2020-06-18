"""Logging configuration for std file, error file and console output."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} | {asctime} | {module}: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} | {module}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'debug_file': {
            'delay': True,
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1000000,  # 1MB ~ 20k rows
            'backupCount': 5,
            'filename': (os.path.join(BASE_DIR, 'cukeweb', 'logs', 'main.log')),
            'formatter': 'verbose',
        },
        'error_file': {
            'delay': True,
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1000000,  # 1MB ~ 20k rows
            'backupCount': 5,
            'filename': (os.path.join(BASE_DIR, 'cukeweb', 'logs', 'error.log')),
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['debug_file', 'error_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
