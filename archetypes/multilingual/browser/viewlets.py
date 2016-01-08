# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.multilingual.interfaces import ILanguage
from plone.app.multilingual.interfaces import ITranslatable
from plone.app.multilingual.browser.viewlets import AddFormIsATranslationViewlet


class addFormATIsATranslationViewlet(AddFormIsATranslationViewlet):
    """ Notify the user that this add form is a translation
    """
    available = False

    def update(self):
        """ It's only for AT on factory so we check """
        # logger.info('Viewlets update, tg: {}'.format(self.request.translation_info['tg']))
        factory = getToolByName(self.context, 'portal_factory', None)
        if factory is None or not factory.isTemporary(self.context):
            return
        super(AddFormIsATranslationViewlet, self).update()
