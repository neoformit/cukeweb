bind = "127.0.0.1"
workers = 2
timeout = 1000

# Environment variables
raw_env = [
    "DJANGO_SETTINGS_MODULE=cukeweb.settings.production",
    "DJANGO_ENV_PATH=/home/admin-cucumber/env.yaml"
    ]
