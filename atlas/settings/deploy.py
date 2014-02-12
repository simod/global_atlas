from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '',
        'HOST': '',
        'USER': '',
        'PASSWORD': '',
        'PORT': 5432
    }
}

STATIC_ROOT = 'static_root'
