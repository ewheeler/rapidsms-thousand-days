import os
import copy
from thousand.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [ '.vagrant.localhost', '.vagrant.curta.local' ]

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

LOGGING['handlers']['rapidsms_file']['filename'] = \
    os.path.join(PROJECT_ROOT, 'rapidsms-router.log')

COMPRESS_ENABLED = True

# ALLOWED_HOSTS needs to be set or Django will 500.
# But our nginx config rejects bad hosts in requests, so we can just
# wildcard this for Django.
ALLOWED_HOSTS = ['*']

LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}
LOGGING['root'] = {
    'level': 'WARNING',
    'handlers': ['sentry'],
}
LOGGING['loggers']['raven'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
    'propagate': False,
}
LOGGING['loggers']['sentry.errors'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
    'propagate': False,
}

# raven docs say to put SentryResponseErrorIdMiddleware
# 'as high in the chain as possible'
TEMP = list(copy.copy(MIDDLEWARE_CLASSES))
TEMP.insert(0, 'raven.contrib.django.raven_compat.'
               'middleware.SentryResponseErrorIdMiddleware')
TEMP.append('raven.contrib.django.raven_compat.'
            'middleware.Sentry404CatchMiddleware')
TEMP.append('siteauth.middleware.SiteAuthenticationMiddleware')
MIDDLEWARE_CLASSES = tuple(TEMP)

INSTALLED_APPS += ("raven.contrib.django.raven_compat",)

# TODO separate staging and prod configs
RAVEN_CONFIG = {
    'dsn': 'https://ca900f5daeee45fe90fdf8d0763d17b4:'
           '021fe82debde4c4f9017e89250bbfcc8@app.getsentry.com/10728',
}

SENTRY_URL = "https://app.getsentry.com/rapidsms/thousand-days/"

CELERY_QUEUES["sentry"] = {
    "exchange": "default",
    "binding_key": "sentry"
}

# For non-publicly accessible applications, the siteauth app can be used to
# restrict access site-wide.
SITEAUTH_ACCESS_ORDER = 'allow/deny'

# whitelist of urls allowing non-authenticated access
SITEAUTH_ALLOW_URLS = (
    r'^$',
    r'^accounts/',
    r'^admin/',
)

SERRANO_AUTH_REQUIRED = False
SERRANO_TOKEN_TIMEOUT = 1200
