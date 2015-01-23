# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import _createObjectByType
from plone.app.multilingual.interfaces import ITranslationManager


def makeContent(context, type_name, id='doc', **kwargs):
    _createObjectByType(type_name, context, id=id, **kwargs)
    obj = context[id]
    obj.reindexObject()
    return obj


def makeTranslation(content, language='en'):
    manager = ITranslationManager(content)
    manager.add_translation(language)
    return manager.get_translation(language)
