import os
import copy
from thousand.settings.base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.vagrant.localhost:8089', '.vagrant.curta.local:8089',
                 '.vagrant.localhost', '.vagrant.curta.local']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thousand',
        'USER': 'postgres',
        'HOST': '127.0.0.1',
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

STATSD_TRACK_MIDDLEWARE = False

# raven docs say to put SentryResponseErrorIdMiddleware
# 'as high in the chain as possible'
TEMP = list(copy.copy(MIDDLEWARE_CLASSES))
TEMP.insert(0, 'raven.contrib.django.raven_compat.'
               'middleware.SentryResponseErrorIdMiddleware')
# add statsd at the top
if STATSD_TRACK_MIDDLEWARE:
    TEMP.insert(0, 'django_statsd.middleware.StatsdMiddleware')

TEMP.append('raven.contrib.django.raven_compat.'
            'middleware.Sentry404CatchMiddleware')
TEMP.append('siteauth.middleware.SiteAuthenticationMiddleware')

if STATSD_TRACK_MIDDLEWARE:
    # add statsd timer at the bottom
    TEMP.append('django_statsd.middleware.StatsdMiddlewareTimer')

MIDDLEWARE_CLASSES = tuple(TEMP)

INSTALLED_APPS += ("raven.contrib.django.raven_compat",)
if STATSD_TRACK_MIDDLEWARE:
    INSTALLED_APPS += ("django_statsd",)

# TODO separate staging and prod configs
RAVEN_CONFIG = {
    'dsn': 'http://a398c13c314241abb98cbcf724ac9ba9:'
           'd17d84bf26fd498eb1f318e5ca86348a@sentry.unicefuganda.org/9',
}

SENTRY_URL = "http://sentry.unicefuganda.org/t4d/thousand-days/"

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
