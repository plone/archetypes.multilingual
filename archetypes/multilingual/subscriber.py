from Acquisition import aq_parent
from zope.component.hooks import getSite
from zope.component import getUtility
from zope.component import queryAdapter
from zope.event import notify
from zope.lifecycleevent import Attributes
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from Products.CMFCore.utils import getToolByName

from archetypes.multilingual.interfaces import IArchetypesTranslatable

from plone.multilingual.interfaces import ILanguage
from plone.multilingual.interfaces import ITranslatable
from plone.multilingual.interfaces import ILanguageIndependentFieldsManager
from plone.multilingual.interfaces import ITranslationManager

from Products.CMFPlone.interfaces import IPloneSiteRoot


class LanguageIndependentModifier(object):
    """Class to handle archetypes editions."""

    stack = []

    def __call__(self, content, event):
        """Called by the event system."""
        if IArchetypesTranslatable.providedBy(content):
            if IObjectModifiedEvent.providedBy(event):
                self.handle_modified(content)

    def handle_modified(self, content):
        canonical = ITranslationManager(content).query_canonical()
        if canonical in self.stack:
            return
        else:
            self.stack.append(canonical)

            # Copy over all language independent fields
            translations = self.get_all_translations(content)
            manager = ILanguageIndependentFieldsManager(content)
            for translation in translations:
                manager.copy_fields(translation)

            schema = content.Schema()
            descriptions = Attributes(schema)
            self.reindex_translations(translations, descriptions)
            self.stack.remove(canonical)

    def reindex_translations(self, translations, descriptions):
        """Once the modifications are done, reindex all translations"""
        for translation in translations:
            translation.reindexObject()
            notify(ObjectModifiedEvent(translation, descriptions))

    def get_all_translations(self, content):
        """Return all translations excluding the just modified content"""
        translations_list_to_process = []
        content_lang = queryAdapter(content, ILanguage).get_language()
        canonical = ITranslationManager(content)
        translations = canonical.get_translations()

        for language in translations.keys():
            if language != content_lang:
                translations_list_to_process.append(translations[language])
        return translations_list_to_process

handler = LanguageIndependentModifier()

