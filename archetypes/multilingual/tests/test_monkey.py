# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from archetypes.multilingual.testing import \
    ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING
from archetypes.multilingual.tests.utils import makeContent
from plone.app.multilingual.interfaces import ILanguage
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing.z2 import Browser

import transaction
import unittest2 as unittest

auth_header = 'Basic {0:s}:{1:s}'.format(TEST_USER_NAME, TEST_USER_PASSWORD)


class TestLanguageMonkeyPatch(unittest.TestCase):

    layer = ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.portal_url = self.portal.absolute_url()
        self.ltool = getToolByName(self.portal, 'portal_languages')
        self.ltool.addSupportedLanguage('ca')
        self.ltool.addSupportedLanguage('es')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_monkey_non_folderish(self):
        self.browser.addHeader('Authorization', auth_header)

        folder = makeContent(self.portal, 'Folder', id='folder')
        ILanguage(folder).set_language('ca')
        transaction.commit()

        self.browser.open('{0:s}/createObject?type_name=Document'.format(
            folder.absolute_url()))
        self.browser.getControl(name="title").value = "doc"
        self.browser.getControl(name="text").value = "BLABLA"
        self.browser.getControl(name="form.button.save").click()

        self.assertEqual(ILanguage(folder['doc']).get_language(), 'ca')

    def test_monkey_folderish(self):
        self.browser.addHeader('Authorization', auth_header)

        folder = makeContent(self.portal, 'Folder', id='folder')
        ILanguage(folder).set_language('ca')
        transaction.commit()

        self.browser.open('{0:s}/createObject?type_name=Document'.format(
            folder.absolute_url()))
        self.browser.getControl(name="title").value = "subfolder"
        self.browser.getControl(name="form.button.save").click()

        self.assertEqual(ILanguage(folder['subfolder']).get_language(), 'ca')
