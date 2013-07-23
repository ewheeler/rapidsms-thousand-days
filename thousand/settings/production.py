from thousand.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'thousand'
DATABASES['patients']['NAME'] = 'patients'

EMAIL_SUBJECT_PREFIX = '[Thousand Prod] '

LOGGING['handlers']['file']['level'] = 'INFO'
LOGGING['handlers']['file']['filename'] = '/var/log/thousand/rapidsms.log'
