# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
from Products.CMFCore.utils import getToolByName


def default_language(self):
    language_tool = getToolByName(self, 'portal_languages')
    if language_tool.startNeutral():
        language = u""
    else:
        language = language_tool.getDefaultLanguage()
    return language
