# -*- coding: utf-8 -*-
from zope import interface

from plone.multilingual.interfaces import ILanguageIndependentFieldsManager

class LanguageIndependentFieldsManager(object):
    interface.implements(ILanguageIndependentFieldsManager)

    def get_field_names(self):
        # TODO
        return

    def copy_fields(self, translation):
        # TODO
        return
