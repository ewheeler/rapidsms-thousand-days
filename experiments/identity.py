from cleaver.identity import CleaverIdentityProvider


class RapidSMSIdentityProvider(CleaverIdentityProvider):

    def __init__(self, environ_key='REMOTE_ADDR'):
        self.environ_key = environ_key

    def get_identity(self, environ):
        return environ[self.environ_key]
