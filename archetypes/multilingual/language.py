# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.multilingual.interfaces import ILanguage
from plone.app.multilingual.interfaces import LANGUAGE_INDEPENDENT
from zope import interface
from zope.component.hooks import getSite


class ATLanguage(object):

    interface.implements(ILanguage)

    def __init__(self, context):
        self.context = context

    def get_language(self):
        language = self.context.Language()
        pf = getToolByName(self.context, 'portal_factory', None)
        if pf is not None and pf.isTemporary(self.context):
            # get the folder portal_factory was invoked in
            context = aq_parent(aq_parent(aq_parent(aq_inner(self.context))))
            navroot = getNavigationRootObject(context, getSite())
            if navroot != self.context:
                language = ILanguage(navroot).get_language()
        if not language:
            language = LANGUAGE_INDEPENDENT
        return language

    def set_language(self, language):
        # Override the setLanguage method imposed by LP
        # and access to the direct mutator of the object
        self.context.getField('language').set(self.context, language)
