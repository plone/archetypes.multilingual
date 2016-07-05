# -*- coding: utf-8 -*-
from plone.app.multilingual.interfaces import ILanguageIndependentFieldsManager
from plone.app.multilingual.interfaces import ITranslationCloner
from zope import interface


@interface.implementer(ITranslationCloner)
class Cloner(object):

    def __init__(self, context):
        self.context = context

    def __call__(self, obj):
        li_clonner = ILanguageIndependentFieldsManager(self.context)
        li_clonner.copy_fields(obj)
