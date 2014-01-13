from .base import *

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

INSTALLED_APPS += ('south',)