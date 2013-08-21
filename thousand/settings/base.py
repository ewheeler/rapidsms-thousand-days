# Django settings for thousand project.

import os

# The top directory for this project. Contains requirements/, manage.py,
# and README.rst, a thousand directory with settings etc (see
# PROJECT_PATH), as well as a directory for each Django app added to this
# project.
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir))
# The directory with this project's templates, settings, urls, static dir,
# wsgi.py, fixtures, etc.
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

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

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

ALLOWED_HOSTS = ['.localhost', '.curta.local']

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/public/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/public/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files to collect
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wat'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'openmrs.context_processors.static',
    'xray.context_processors.web_experiments',
    'thousand.context_processors.template_variables',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'serrano.middleware.SessionMiddleware',
)

ROOT_URLCONF = 'thousand.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'thousand.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

# A sample logging configuration.
# This logs all rapidsms messages to the file `rapidsms.log`
# in the project directory.  It also sends an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'rapidsms_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_PATH, 'rapidsms-router.log'),
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'rapidsms': {
            'handlers': ['rapidsms_file'],
            'propagate': True,
            'level': 'DEBUG',
        },

    }
}

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",

    # External apps
    "django_nose",
    #"djtables",  # required by rapidsms.contrib.locations
    "django_tables2",
    "selectable",
    "south",
    "kombu.transport.django",
    "djcelery",

    # RapidSMS
    "rapidsms",
    "rapidsms.backends.database",
    "rapidsms.contrib.handlers",
    "rapidsms.contrib.httptester",
    "rapidsms.contrib.messagelog",
    "rapidsms.contrib.messaging",
    "rapidsms.contrib.registration",

    # Thousand Days
    "thousand.backends.openmrs",
    "nutrition",
    "appointments",
    "natalcare",
    "xray",

    # Harvest stack
    "django.contrib.markup",
    "django.contrib.humanize",
    "openmrs",
    "openmrs.drugs",
    "openmrs.vaccines",
    "openmrs.diagnoses",
    "haystack",
    "avocado",
    "serrano",
    "rapidsms.contrib.default",  # Must be last
)

INSTALLED_BACKENDS = {
    "message_tester": {
        "ENGINE": "rapidsms.backends.database.DatabaseBackend",
    },
}

HEALTHCARE_STORAGE_BACKEND = "thousand.backends.openmrs.storage.DjangoStorage"

LOGIN_REDIRECT_URL = '/'

RAPIDSMS_HANDLERS = (
    'rapidsms.contrib.echo.handlers.echo.EchoHandler',
    'rapidsms.contrib.echo.handlers.ping.PingHandler',
    'nutrition.handlers.CreateReportHandler',
    'nutrition.handlers.CancelReportHandler',
    'appointments.handlers.confirm.ConfirmHandler',
    'appointments.handlers.move.MoveHandler',
    'appointments.handlers.new.NewHandler',
    'appointments.handlers.quit.QuitHandler',
    'appointments.handlers.status.StatusHandler',
    'natalcare.handlers.birth.BirthHandler',
    'natalcare.handlers.pregnancy.PregnancyHandler',
)

# django-celery config
import djcelery
djcelery.setup_loader()

from celery.schedules import crontab
BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ("appointments.tasks", )
CELERY_QUEUES = {
    "default": {
        "exchange": "default",
        "binding_key": "default"},
}
CELERYBEAT_SCHEDULE = {
    'generate-appointments': {
        'task': 'appointments.tasks.generate_appointments',
        'schedule': crontab(minute=1),
    },
    'send-notifications': {
        'task': 'appointments.tasks.send_appointment_notifications',
        'schedule': crontab(minute=5),
    },
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'serrano.backends.TokenBackend',
)


DATABASE_ROUTERS = ['thousand.dbrouters.PatientRouter', ]

# Haystack
HAYSTACK_SITECONF = 'avocado.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_PATH, 'whoosh.index')

MODELTREES = {
    'default': {
        'model': 'openmrs.patient',
    }
}

SERRANO_CORS_ENABLED = True
SERRANO_AUTH_REQUIRED = False
SERRANO_TOKEN_TIMEOUT = 1200

# SESSIONS AND COOKIES

CSRF_COOKIE_NAME = 'openmrs_csrftoken'
