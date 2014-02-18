from thousand.settings.staging import *

# There should be only minor differences from staging
ALLOWED_HOSTS = ['.thousand-days.lobos.biz',
                 '.omega.unicefuganda.org',
                 '127.0.0.1:8000']
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
