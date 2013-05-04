# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def isVisible(self, instance, mode='view'):
    '''monkey patching visibility of Products.Archetypes.Widget.LanguageWidget
       but only if plone.multilingual is activated in quickinstaller for given plone site'''
    qi=getToolByName(instance,'portal_quickinstaller')
    if (qi.isProductInstalled('plone.multilingual')):
        return 'invisible'   
    else:
        return 'visible'   #preserves language widget for non pam sites