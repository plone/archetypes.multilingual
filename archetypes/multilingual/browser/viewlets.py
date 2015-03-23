# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFPlone.interfaces import ILanguage
from plone.app.multilingual.interfaces import ITranslatable


class addFormATIsATranslationViewlet(ViewletBase):
    """ Notice the user that this add form is a translation
    """
    available = False

    def language(self):
        return self.lang

    def origin(self):
        return self.origin

    def render(self):
        if self.available:
            return self.index()
        return u""

    def update(self):
        """ It's only for AT on factory so we check """
        if self.context.portal_factory.isTemporary(self.context):
            if ITranslatable.providedBy(self.context):
                self.lang = ILanguage(self.context).get_language()
            else:
                self.lang = 'NaN'
            # No support for sessions on PAM
            # Its needed to be done an implementation to pass the tg to
            # to the factory
            # if 'tg' in session.keys():
            #     tg = session['tg']
            #     self.available = True
            #     ptool = getToolByName(self.context, 'portal_catalog')
            #     query = {'TranslationGroup': tg, 'Language': 'all'}
            #     results = ptool.searchResults(query)
            #     self.origin = results
