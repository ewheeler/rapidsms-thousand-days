import logging

logger = logging.getLogger('rapidsms')

from django.conf import settings

from cleaver.base import Cleaver
from cleaver.identity import CleaverIdentityProvider
from cleaver.backend import CleaverBackend
from cleaver.backend.db import SQLAlchemyBackend

from rapidsms.apps.base import AppBase

from .identity import SMSIdentityProvider


class App(AppBase):

    def __init_cleaver(self, cleaver_identity, cleaver_backend):
        if not isinstance(cleaver_identity, CleaverIdentityProvider) and \
                not callable(cleaver_identity):
            raise RuntimeError(
                '%s must be callable or implement '
                'cleaver.identity.CleaverIdentityProvider' % cleaver_identity
            )
        if not isinstance(cleaver_backend, CleaverBackend):
            raise RuntimeError(
                '%s must implement cleaver.backend.CleaverBackend' % cleaver_backend
            )
        self._cleaver_backend = cleaver_backend
        self._cleaver_identity = cleaver_identity

    def __init__(self, router):
        self.__init_cleaver(SMSIdentityProvider(),
                          SQLAlchemyBackend(settings.CLEAVER_DATABASE))

    def filter(self, message):

        # add connection to message metadata because
        # only the metadata (not the message object)
        # is passed to cleaver
        message.fields.update({'connection': message.connection})

        cleaver = Cleaver(
            message.fields,
            self._cleaver_identity,
            self._cleaver_backend
        )
        message.fields.update({'cleaver': cleaver})

        # Mark the visitor as a human
        self._cleaver_backend.mark_human(cleaver.identity)

        # If the visitor has been assigned any experiment variants,
        # tally their participation.
        for e in self._cleaver_backend.all_experiments():
            variant = self._cleaver_backend.get_variant(
                cleaver.identity,
                e.name
            )
            if variant:
                self._cleaver_backend.mark_participant(e.name, variant)

    def handle(self, message):

        if message.text.startswith('wat'):
            cleaver = message.fields['cleaver']
            # test a few responses to 'wat'
            response = cleaver(
                'wat_response_experiment',
                ('foo', 'foo'),
                ('bar', 'bar'),
                ('baz', 'baz')
            )
            message.respond(response)
            return True

        if message.text.startswith('huh'):
            # score conversion if user sends 'huh'
            # note this conversion could be scored in
            # another app or handler because the cleaver
            # object is added to the message's fields
            # property during the `filter` phase
            cleaver = message.fields['cleaver']
            cleaver.score('wat_response_experiment')
