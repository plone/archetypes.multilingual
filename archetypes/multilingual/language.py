# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
from plone.multilingual.interfaces import (
    ILanguage,
    LANGUAGE_INDEPENDENT,
)
from zope import interface


class ATLanguage(object):

    interface.implements(ILanguage)

    def __init__(self, context):
        self.context = context

    def get_language(self):
        language = self.context.Language()
        if not language:
            language = LANGUAGE_INDEPENDENT
        return language

    def set_language(self, language):
        self.context.setLanguage(language)
