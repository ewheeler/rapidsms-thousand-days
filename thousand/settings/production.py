from thousand.settings.staging import *

TIME_ZONE = 'Africa/Kampala'
LANGUAGE_CODE = 'en-UG'
COUNTRY_CODES = ('UG',)

# disable L10N because django does not format
# dates appropriately for 'en-UG'
USE_L10N = False
DATE_FORMAT = 'j N Y'
DATETIME_FORMAT = 'H:i T j N Y'
SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'H:i d/m/Y'

# There should be only minor differences from staging
ALLOWED_HOSTS = ['.omega.unicefuganda.org',
                 '127.0.0.1',
                 '196.0.26.59']
EMAIL_SUBJECT_PREFIX = '[Thousand Prod] '

INSTALLED_BACKENDS = {
    "kannel-yo": {
        "ENGINE": "rapidsms.backends.kannel.KannelBackend",
        "sendsms_url": "http://127.0.0.1:13013/cgi-bin/sendsms",
        "sendsms_params": {"smsc": "smpp",
                           "from": "6400",
                           "username": "kannel",
                           "password": "kannel"},
        "coding": 0,
        "charset": "ascii",
        "encode_errors": "ignore",
    },
}

LOGGING['handlers']['rapidsms_file']['filename'] = '/var/www/thousand-production/log/rapidsms-router.log'
