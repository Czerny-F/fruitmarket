"""Settings for development environment."""
import os
from .base import *  # noqa

ENVIRONMENT = 'development'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h83_&&&q0q*&ms&e0*&v#uue51=b_$*f^9=nbf)+ev(ei8le7%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

ROOT_URLCONF = 'fruitmarket.urls.development'

WSGI_APPLICATION = 'fruitmarket.wsgi.application'


# Django Debug Toolbar

INSTALLED_APPS += [  # noqa
    'debug_toolbar',
]

MIDDLEWARE += [  # noqa
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),  # noqa
    }
}


# Static files for local

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')  # noqa
