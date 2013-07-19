import os
from thousand.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SERRANO_AUTH_REQUIRED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'dev-thousand.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'patients': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'patients.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

LOGGING['handlers']['rapidsms_file']['filename'] = os.path.join(PROJECT_ROOT, 'rapidsms-router.log')

COMPRESS_ENABLED = True

# ALLOWED_HOSTS needs to be set or Django will 500.
# But our nginx config rejects bad hosts in requests, so we can just
# wildcard this for Django.
ALLOWED_HOSTS = ['*']

# TODO set this via salt and/or fabric
CLEAVER_DATABASE = 'sqlite:////home/ewheeler/www/staging/thousand/experiments/experiment.data'
