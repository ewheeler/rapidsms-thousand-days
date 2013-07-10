import hashlib
import logging
from cleaver.identity import CleaverIdentityProvider

logger = logging.getLogger('rapidsms')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'thousand.settings.local'

from django.conf import settings
SessionStore = __import__(settings.SESSION_ENGINE, fromlist=['']).SessionStore

# thanks to http://mobiforge.com/forum/running/analytics/stats-and-unique-vistors-different-mobile
# and
# http://mobiforge.com/developing/blog/useful-x-headers
headers_for_fingerprint = ['USER-AGENT', 'HOST', 'ACCEPT', 'ACCEPT-LANGUAGE', 'ACCEPT-CHARSET', 'X-REAL-IP', 'X-FORWARDED-HOST', 'X-FORWARDED-SERVER', 'X-FORWARDED-FOR', 'X-UP-SUBNO', 'X-NOKIA-MSISDN', 'X-UP-CALLING-LINE-ID', 'X-HTS-CLID', 'X-H3G-MSISDN', 'X-NX-CLID', 'X-ACCESS-SUBNYM', 'X-ORANGE-ID', 'MSISDN', 'X-WAP-PROFILE', 'X-WAP-PROFILE-DIFF', 'X-APN-ID', 'X-DRUTT-DEVICE-ID', 'X-DRUTT-PORTAL-USER-ID', 'X-DRUTT-PORTAL-USER-MSISDN', 'X-GGSNIP', 'X-JPHONE-COLOR', 'X-JPHONE-DISPLAY', 'X-NETWORK-INFO', 'X-OS-PREFS', 'X-NOKIA-ALIAS', 'X-NOKIA-BEARER', 'X-NOKIA-IMSI', 'X-NOKIA-MSISDN', 'X-OPERAMINI-PHONE', 'X-ORIGINAL-USER-AGENT', 'X-IMSI', 'X-MSISDN']


class WebIdentityProvider(CleaverIdentityProvider):

    def fingerprint(environ):
        header_info = []
        headers_upper = dict((k.upper(), v) for k, v in environ.iteritems() if isinstance(v, str))
        for header in headers_for_fingerprint:
            header_info.append(headers_upper.get(header, ''))
        fingerprint = hashlib.md5(''.join(header_info)).hexdigest()
        return fingerprint

    def _find_identity(self, environ):
        if 'HTTP_COOKIE' in environ:
            cookie = {s.split('=')[0].strip(): s.split('=')[1].strip() for s in environ['HTTP_COOKIE'].split(';')}
            if 'sessionid' in cookie:
                environ['session_key'] = cookie['sessionid']
                session = SessionStore(session_key=cookie['sessionid'])
                if session.exists(cookie['sessionid']):
                    session.load()
                    user_id = session.get('_auth_user_id')
                    # From here, you can load your user's django object
                    # and attach it to the environ object
                    # for example:
                    if user_id is not None:
                        from django.contrib.auth.models import User
                        environ['CURRENT_USER'] = User.objects.get(id=user_id)
                        return user_id
            # if user is not logged in, use sessionid
            return cookie['sessionid']
        return self.fingerprint(environ)

    def get_identity(self, environ):
        return self._find_identity(environ)


class SMSIdentityProvider(CleaverIdentityProvider):

    def get_identity(self, message_fields):
        # create hash of backend name and identity
        id_str = message_fields['connection'].backend.name + message_fields['connection'].identity
        cleaver_id = hashlib.md5(id_str).hexdigest()
        message_fields.update({'cleaver_id': cleaver_id})
        return cleaver_id
