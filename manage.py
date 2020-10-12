### GETING STARTED WITH A NEW DJANGO PROJECT.

## Create a virtual environment to isolate our package dependencies locally
# python3 -m venv env
# source env/bin/activate  # On Windows use `env\Scripts\activate`

## Install Django and Django REST framework into the virtual environment
# pip install django
# pip install djangorestframework

## Set up a new project with a single application
# django-admin startproject tutorial .
# django-admin startapp quickstart
# python manage.py migrate
# python manage.py createsuperuser --email admin@example.com --username admin
# python manage.py runserver
# app is now accessible on http://127.0.0.1:8000/

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# False if not in os.environ
DEBUG = env('DEBUG')

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
# SECRET_KEY = env('SECRET_KEY')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dontlook.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# TODO create folder logs

if __name__ == '__main__':
    main()
