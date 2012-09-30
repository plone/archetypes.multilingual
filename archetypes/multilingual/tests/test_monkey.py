import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.app.testing import login

from archetypes.multilingual.tests._testing import ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING

from archetypes.multilingual.tests.utils import makeContent

from plone.multilingual.interfaces import ILanguage

import transaction


class TestLanguageMonkeyPatch(unittest.TestCase):

    layer = ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.portal_url = self.portal.absolute_url()
        language_tool = getToolByName(self.portal, 'portal_languages')
        language_tool.addSupportedLanguage('ca')
        language_tool.addSupportedLanguage('es')

    def test_monkey_non_folderish(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD))
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        folder = makeContent(self.portal, 'Folder', id='folder')
        ILanguage(folder).set_language('ca')
        transaction.commit()

        self.browser.open(folder.absolute_url() + '/createObject?type_name=Document')
        self.browser.getControl(name="title").value = "doc"
        self.browser.getControl(name="text").value = "BLABLA"
        self.browser.getControl(name="form.button.save").click()

        self.assertEqual(ILanguage(folder['doc']).get_language(), 'ca')

    def test_monkey_folderish(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD))
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        folder = makeContent(self.portal, 'Folder', id='folder')
        ILanguage(folder).set_language('ca')
        transaction.commit()

        self.browser.open(folder.absolute_url() + '/createObject?type_name=Folder')
        self.browser.getControl(name="title").value = "subfolder"
        self.browser.getControl(name="form.button.save").click()

        self.assertEqual(ILanguage(folder['subfolder']).get_language(), 'ca')
