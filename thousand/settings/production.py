from thousand.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'thousand'
DATABASES['patients']['NAME'] = 'patients'

EMAIL_SUBJECT_PREFIX = '[Thousand Prod] '

LOGGING['handlers']['file']['level'] = 'INFO'
LOGGING['handlers']['file']['filename'] = '/var/log/thousand/rapidsms.log'

# TODO set this via salt and/or fabric
CLEAVER_DATABASE = 'sqlite:////home/ewheeler/www/staging/thousand/experiments/experiment.data'
