# -*- coding: utf-8 -*-

import transaction
import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from plone.app.multilingual.interfaces import ILanguage
from plone.app.multilingual.interfaces import LANGUAGE_INDEPENDENT
from archetypes.multilingual.testing import \
    ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.testing.z2 import Browser
from zope.interface import alsoProvides


auth_header = 'Basic {0:s}:{1:s}'.format(TEST_USER_NAME,
                                         TEST_USER_PASSWORD)


class TestATILanguage(unittest.TestCase):

    layer = ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.portal_url = self.portal.absolute_url()
        self.ltool = getToolByName(self.portal, 'portal_languages')
        self.ltool.addSupportedLanguage('ca')
        self.ltool.addSupportedLanguage('es')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_real_content_with_lang(self):
        portal = self.portal
        portal.invokeFactory(type_name='Document', id='doc')
        ILanguage(portal.doc).set_language('de')
        self.assertEqual(ILanguage(portal.doc).get_language(), 'de')

    def test_real_content_no_lang(self):
        portal = self.portal
        portal.invokeFactory(type_name='Document', id='doc')
        self.assertEqual(ILanguage(portal.doc).get_language(),
                         LANGUAGE_INDEPENDENT)

    def test_real_content_in_folder(self):
        portal = self.portal
        self.portal.invokeFactory(type_name='Folder', id='folder')
        ILanguage(portal.folder).set_language('de')
        portal.folder.invokeFactory(type_name='Document', id='doc')
        self.assertEqual(ILanguage(portal.folder.doc).get_language(), 'de')

    def test_temp_content_root_folder(self):
        portal = self.portal
        self.portal.invokeFactory(type_name='Folder', id='folder1')
        self.browser.addHeader('Authorization', auth_header)
        ILanguage(portal.folder1).set_language('de')
        alsoProvides(portal.folder1, INavigationRoot)
        transaction.commit()
        self.browser.open('{0:s}/createObject?type_name=Document'.format(
            portal.folder1.absolute_url()))
        self.browser.getControl(name="title").value = "doc"
        self.browser.getControl(name="form.button.save").click()
        self.assertEqual(ILanguage(portal.folder1.doc).get_language(), 'de')
