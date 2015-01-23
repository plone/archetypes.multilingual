# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from archetypes.multilingual.testing import \
    ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING
from plone.app.multilingual.interfaces import ILanguage
from plone.app.multilingual.interfaces import ITranslatable
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

import unittest


def makeContent(context, type_name, id='doc', **kwargs):
    _createObjectByType(type_name, context, id=id, **kwargs)
    obj = context[id]
    obj.reindexObject()
    return obj


class TestArchetypesLanguageInheritance(unittest.TestCase):

    layer = ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.ltool = getToolByName(self.portal, 'portal_languages')
        self.ltool.addSupportedLanguage('de')
        self.ltool.addSupportedLanguage('en')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.lrf_de = makeContent(self.portal, 'LRF', id='de')
        ILanguage(self.lrf_de).set_language('de')
        self.lrf_en = makeContent(self.portal, 'LRF', id='en')
        ILanguage(self.lrf_en).set_language('en')
        self.lri_neutral = makeContent(self.portal, 'LRF', id='neutral')

    def test_archetype_provides_interface_when_located_in_lri(self):
        sample_id = self.lri_neutral.invokeFactory('Document', 'd1')
        sample = self.lri_neutral[sample_id]
        self.assertTrue(ITranslatable.providedBy(sample))

    def test_archetype_provides_interface_when_located_in_lrf(self):
        sample_id = self.lrf_de.invokeFactory('Document', 'd1')
        sample = self.lrf_de[sample_id]
        self.assertTrue(ITranslatable.providedBy(sample))

    def test_content_in_LRI(self):
        doc_id = self.lri_neutral.invokeFactory('Document', 'lri-document')
        doc = self.lri_neutral[doc_id]

        self.assertEqual(ILanguage(doc).get_language(), '')

    def test_content_in_LRF(self):
        doc_id = self.lrf_de.invokeFactory('Document', 'de-document')
        doc = self.lrf_de[doc_id]

        self.assertEqual(ILanguage(doc).get_language(), 'de')

    def test_content_moved_from_LRI_into_LRF(self):
        doc_id = self.lri_neutral.invokeFactory('Document', 'lri-document')
        doc = self.lri_neutral[doc_id]

        self.assertEqual(ILanguage(doc).get_language(), '')

        # now we move the doc into 'de' folder and the language should be
        # automatically set to 'de'.
        self.lrf_de.manage_pasteObjects(
            self.lri_neutral.manage_copyObjects(ids=[doc_id]))

        doc = self.lrf_de[doc_id]
        self.assertEqual(ILanguage(doc).get_language(), 'de')

    def test_content_moved_from_LRF_into_LRI(self):
        doc_id = self.lrf_de.invokeFactory('Document', 'lri-document')
        doc = self.lrf_de[doc_id]

        self.assertEqual(ILanguage(doc).get_language(), 'de')

        # now we move the doc into 'de' folder and the language should be
        # automatically set to 'de'.
        self.lri_neutral.manage_pasteObjects(
            self.lrf_de.manage_copyObjects(ids=[doc_id]))

        doc = self.lri_neutral[doc_id]
        self.assertEqual(ILanguage(doc).get_language(), '')
