from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from plone.app.multilingual.interfaces import ILanguage

from plone.app.multilingual.interfaces import ITranslationManager
from plone.testing.z2 import Browser
from archetypes.multilingual.testing import \
    ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING
import transaction
import unittest2 as unittest
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.testing import login
from plone.app.testing import setRoles

auth_header = 'Basic {0:s}:{1:s}'.format(TEST_USER_NAME, TEST_USER_PASSWORD)


class TestFactory(unittest.TestCase):

    layer = ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        # Define available languages
        language_tool = getToolByName(self.portal, 'portal_languages')
        language_tool.addSupportedLanguage('fr')
        language_tool.addSupportedLanguage('nl')

        # Enable request negotiator
        language_tool.use_request_negotiation = True

        # Setup language root folders
        setup_tool = SetupMultilingualSite()
        setup_tool.setupSite(self.portal)
        self.lrf_fr = self.portal.fr
        self.lrf_nl = self.portal.nl
        self.browser = Browser(self.layer['app'])

    def test_factory_creation(self):
        self.browser.addHeader('Authorization', auth_header)

        doc_fr_id = self.lrf_fr.invokeFactory('Document', 'fr-document')
        doc_fr = self.lrf_fr[doc_fr_id]
        # ILanguage(folder).set_language('fr')
        transaction.commit()

        self.browser.open('{0:s}/@@create_translation?language=nl'.format(doc_fr.absolute_url()))
        self.assertIn(
            'id="babel-edit"', self.browser.contents)

    def test_factory_creation_on_private_folder(self):
        self.browser.addHeader('Authorization', auth_header)

        doc_fr_id = self.lrf_fr.invokeFactory('Document', 'fr-document')
        doc_fr = self.lrf_fr[doc_fr_id]

        # the target folder is "private"
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.doActionFor(self.lrf_nl, 'retract')
        transaction.commit()

        self.browser.open('{0:s}/@@create_translation?language=nl'.format(doc_fr.absolute_url()))
        self.assertIn(
            'id="babel-edit"', self.browser.contents)

    def test_link_between_documents(self):
        self.browser.addHeader('Authorization', auth_header)

        doc_fr_id = self.lrf_fr.invokeFactory('Document', 'fr-document')
        doc_fr = self.lrf_fr[doc_fr_id]
        # ILanguage(folder).set_language('fr')
        transaction.commit()

        self.browser.open('{0:s}/@@create_translation?language=nl'.format(
            doc_fr.absolute_url()))
        self.browser.getControl(name="title").value = "nl-document"
        self.browser.getControl(name="text").value = "Mijn document"
        self.browser.getControl(name="form.button.save").click()
        doc_nl = self.lrf_nl['nl-document']
        self.assertEqual(ILanguage(doc_nl).get_language(), 'nl')
        self.assertIn('Mijn document', self.browser.contents)
        translations = ITranslationManager(doc_nl).get_translations()
        self.assertTrue("fr" in translations.keys(), 'fr language should be in translations')

        translations = ITranslationManager(doc_fr).get_translations()
        self.assertTrue("nl" in translations.keys(), 'nl language should be in translations')
