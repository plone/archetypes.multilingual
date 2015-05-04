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
        portal_factory = getToolByName(self.context, 'portal_factory', None)
        if portal_factory is not None and portal_factory.isTemporary(self.context):
            # This should probably be fixed in plone.app.layout getNavigationRootObject
            # Right now navigation root of a temporary object is Plone site due to acquisition
            # https://github.com/plone/plone.app.layout/issues/57
            # We can manually construct the correct `context`, though...
            context = aq_parent(aq_parent(aq_parent(aq_inner(self.context))))
            navroot = getNavigationRootObject(context, getSite())
            if navroot != self.context:
                try:
                    lang_info = ILanguage(navroot)
                    language = lang_info.get_language()
                except TypeError:
                    # I can still reach this point when translating items outside language folders
                    language = None
        if not language:
            language = LANGUAGE_INDEPENDENT
        return language

    def set_language(self, language):
        # Override the setLanguage method imposed by LP
        # and access to the direct mutator of the object
        self.context.getField('language').set(self.context, language)
        self.context.reindexObject(idxs=['Language'])
