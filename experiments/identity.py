import logging
logger = logging.getLogger('rapidsms')

from cleaver.identity import CleaverIdentityProvider

import rolodex


class WebIdentityProvider(CleaverIdentityProvider):
    def __init__(self):
        self.rolodex = rolodex.Rolodex()

    def get_identity(self, environ):
        identities = self.rolodex.lookup_browser(environ)
        environ['UID'] = identities.get('uid')
        environ['BID'] = identities.get('bid')
        environ['SID'] = identities.get('sid')
        if identities.get('uid') is not None:
            return identities['uid']
        if identities.get('bid') is not None:
            return identities['bid']
        return identities['sid']


class SMSIdentityProvider(CleaverIdentityProvider):
    def __init__(self):
        self.rolodex = rolodex.Rolodex()

    def get_identity(self, message_fields):
        # create hash of backend name and identity
        identities = self.rolodex.lookup_msisdn(message_fields['connection'].identity)
        # TODO use uid if available?
        cleaver_id = identities['mid']
        message_fields.update({'cleaver_id': cleaver_id,
                               'uid': identities.get('uid'),
                               'mid': identities.get('mid')})
        return cleaver_id
