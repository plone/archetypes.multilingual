# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.multilingual.interfaces import ILanguage, ITranslatable


def default_language(self):
    """
        Monkey patch to control the default language from
        new created ATs. It must default to parent's language
        if parent not implements IPloneSiteRoot.
    """
    parent = aq_parent(self)
    language_tool = getToolByName(self, 'portal_languages')
    if language_tool.startNeutral():
        # We leave this untouched by now.
        language = u""
    elif IPloneSiteRoot.implementedBy(parent):
        language = language_tool.getPreferredLanguage()
    elif ITranslatable.providedBy(parent):
        language = ILanguage(parent).get_language()
    return language


def isVisible(self, instance, mode='view'):
    return 'invisible'
