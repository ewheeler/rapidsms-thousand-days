#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import operator
from collections import namedtuple

from rapidsms.apps.base import AppBase
from rapidsms.contrib.handlers.utils import get_handlers
from rapidsms.conf import settings

Action = namedtuple('Action',
                    'handler, prefix, keyword, help_text, help_func')


class App(AppBase):

    def __init__(self, router):
        super(App, self).__init__(router)

        self.handlers = get_handlers()

        if hasattr(settings, 'RAPIDSMS_HELP_KEYWORDS'):
            self.triggers = settings.RAPIDSMS_HELP_KEYWORDS
        else:
            self.triggers = ['HELP', 'AIDE']

        self._gather_keywords()

    def handle(self, msg):

        # expose available handler actions to `help` queries
        # such that `help` returns a list of availaible prefix+keyword
        # actions (as well as bare keyword actions), `help prefix` returns
        # the available keywords within the prefix's scope, and
        # `help prefix keyword` returns the help_text for that handler
        if self.actions:
            tokens = map(operator.methodcaller('upper'), msg.text.split())
            if tokens and (tokens[0] in self.triggers):
                if len(tokens) > 1:
                    if tokens[1] in self.prefixes:
                        matches = list(set(a for a in self.actions
                                           if a.prefix == tokens[1]))
                        keywords = map(operator.attrgetter('keyword'), matches)
                        if len(tokens) > 2:
                            if tokens[2] in keywords:
                                match = [m for m in matches
                                         if m.keyword == tokens[2]]
                                if match:
                                    # sanity check in _gather_keywords should
                                    # raise if there are handler keyword
                                    # collisions, but lets assert that there is
                                    # only 1 matching handler to be extra safe
                                    assert len(match) == 1,\
                                        ('Duplicate keyword "%s" '
                                            'for prefix "%s"') %\
                                        (tokens[1], tokens[2])
                                    # check for help_text to avoid
                                    # sending a blank response
                                    if match[0].help_text:
                                        # TODO standardize help_text template
                                        # TODO this smells like a dodgy way to
                                        # accomodate help_text string templates
                                        # that have `prefix` AND/OR `keyword`
                                        # named substitutions. this should be
                                        # removed in favor of a proper
                                        # `help_text` API for apps and handlers
                                        formatter = FormatStringFromContext(
                                            match[0].help_text,
                                            match[0]._asdict())
                                        msg.respond(formatter.formatted)
                                        return True
                        # TODO i18n
                        msg.respond('Available %(prefix)s keywords: '
                                    '%(keywords)s'
                                    % {'prefix': tokens[1],
                                       'keywords': ', '.join(keywords)})
                        return True

                return self._respond_with_actions(msg)

    def _respond_with_actions(self, msg):
        # join prefix and keyword with a space,
        # then join prefix+keyword pairs with commas
        # TODO i18n
        reply = ('Available actions: %s' %
                (', '.join((' '.join((a.prefix, a.keyword))
                            for a in self.actions))))

        # keywords without a prefix will have two
        # leading spaces, so replace with a single space
        reply = reply.replace('  ', ' ')
        msg.respond(reply)
        return True

    def default(self, msg):
        return self._respond_with_actions(msg)

    def _gather_keywords(self):
        """ This creates Action objects to catalogue the currently-installed
            handlers, their prefixes, their keywords, and their help_text.
            The list of Action objects is used to create responses
            to `help` queries not handled by other apps.
            Also performs sanity check to identify Handler keyword collisions.
        """
        self.actions = []
        self.prefixes = []
        for handler in self.handlers:
            prefix = getattr(handler, 'prefix', '')
            keyword = getattr(handler, 'keyword', '')
            help_text = getattr(handler, 'help_text', '')
            help_func = getattr(handler, 'help', '')

            # build set of prefixes
            if prefix and (prefix.upper() not in self.prefixes):
                self.prefixes.append(prefix.upper())

            if prefix or keyword:
                if prefix and not keyword:
                    # avoid listing bare prefixes as actions.
                    # typical usage of the prefix+keyword pattern
                    # presupposes that all actions are scoped within the
                    # prefix's namespace (e.g., the prefix itself does
                    # nothing)
                    continue

                # some handlers don't have prefix or keyword or help_text
                # attributes, so create namedtuple for convenient access
                # without needing to hasattr all the time.
                self.actions.append(Action._make((handler, prefix.upper(),
                                                  keyword.upper(), help_text,
                                                  help_func)))

        # ensure that prefix+keyword pairs are unique
        pairs = [(a.prefix, a.keyword) for a in self.actions]
        if len(pairs) != len(set(pairs)):
            raise RuntimeError('Handler keyword collision!')


class FormatStringFromContext(object):
    """ This is a hack to easily format old-style
        string formatting templates (e.g., `%(name)s` substitution)
        that might have different named substitution fields.

        For example, if you have the following templates:
            one = "hello my name is %(first)s"
            two = "hello my name is %(first)s %(last)s"

        they can both be accomodated by this class if you define
        values for both `first` and `last` in a provided dict-like context
        such as a my_namedtuple._asdict() (or locals() if you dare)

        Like so:
            my_context = {'first': 'Foo', 'last': 'Bar'}
            my_template = one
            formatter = FormatStringFromContext(my_template, my_context)

            # if you just want to know what named substitutions
            # are present in the template, you can access the list
            # which in this case would be ['first']
            named_substitutions_in_my_template = formatter.substitutions

            # get the formatted string, which in this case is
            # "hello my name is Foo"
            formatted_string = formatter.formatted

            my_template = two
            formatter = FormatStringFromContext(my_template, my_context)

            # if you just want to know what named substitutions
            # are present in the template, you can access the list
            # which in this case would be ['first', 'last']
            named_substitutions_in_my_template = formatter.substitutions

            # get the formatted string, which in this case is
            # "hello my name is Foo Bar"
            formatted_string = formatter.formatted

        This class and its usage should be replaced by a
        sensible API for dealing with app and handler help_text.
    """
    def __init__(self, string_template, context):
        self.substitutions = []
        self.context = context
        # perform the string formating,
        # which will use this class' __getitem__
        self.formatted = string_template % self

    def __getitem__(self, item):
        if item not in self.substitutions:
            # add name of each named substitution to list
            self.substitutions.append(item)
        if item in self.context:
            # use value in given context with same name
            # as the named substition
            # NOTE this will raise if item is not found
            # in the given context
            return self.context[item]
