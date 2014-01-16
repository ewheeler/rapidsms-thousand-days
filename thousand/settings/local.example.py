from thousand.settings.dev import *

# Override settings here
TIME_ZONE = 'Africa/Kampala'
LANGUAGE_CODE = 'en-UG'

# disable L10N because django does not format dates
# appropriately for 'en-UG'
USE_L10N = False
DATE_FORMAT = 'j N Y'
DATETIME_FORMAT = 'H:i T j N Y'
SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'H:i T d/m/Y'
