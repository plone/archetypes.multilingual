# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from archetypes.multilingual.interfaces import IArchetypesTranslatable
from plone.app.multilingual.interfaces import ILanguage
from plone.app.multilingual.interfaces import ILanguageIndependentFieldsManager
from plone.app.multilingual.interfaces import ITranslationManager
from zope.component import queryAdapter
from zope.event import notify
from zope.lifecycleevent import Attributes
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from plone.dexterity.interfaces import IDexterityContent
from plone.app.multilingual.subscriber import set_recursive_language
from plone.app.multilingual.interfaces import IMutableTG
from plone.app.multilingual.interfaces import ITranslatable
from plone.app.multilingual.interfaces import LANGUAGE_INDEPENDENT

from zope.globalrequest import getRequest
from zope.lifecycleevent import modified
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner


class LanguageIndependentModifier(object):
    """Class to handle archetypes editions."""

    stack = []

    def __call__(self, content, event):
        """Called by the event system."""
        if IArchetypesTranslatable.providedBy(content):
            if IObjectModifiedEvent.providedBy(event):
                self.handle_modified(content)

    @property
    def is_translatable(self):
        return not IDexterityContent.providedBy(self.obj)

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


def get_parent(obj):
    portal_factory = getToolByName(obj, 'portal_factory', None)
    if portal_factory is not None and portal_factory.isTemporary(obj):
        # created by portal_factory
        parent = aq_parent(aq_parent(aq_parent(aq_inner(obj))))
    else:
        parent = aq_parent(aq_inner(obj))
    return parent


def archetypes_creation_handler(obj, event):
    """Subscriber to set language on the child folder
    It can be a
    - IObjectRemovedEvent - don't do anything
    - IObjectMovedEvent
    - IObjectAddedEvent
    - IObjectCopiedEvent
    """
    # if not translatable
    if (not IObjectRemovedEvent.providedBy(event)
       and IDexterityContent.providedBy(obj)):
        return

    # On ObjectCopiedEvent and ObjectMovedEvent aq_parent(event.object) is
    # always equal to event.newParent.
    parent = get_parent(event.object)

    # special parent handling
    if not ITranslatable.providedBy(parent):
        set_recursive_language(obj, LANGUAGE_INDEPENDENT)
        return

    # Normal use case
    # We set the tg, linking
    language = ILanguage(parent).get_language()
    set_recursive_language(obj, language)

    request = getattr(event.object, 'REQUEST', getRequest())
    try:
        ti = get_translation_info(request)
    except AttributeError:
        return

    IMutableTG(obj).set(ti['tg'])
    modified(obj)
    tm = ITranslationManager(obj)
    old_obj = tm.get_translation(ti['source_language'])
    ILanguageIndependentFieldsManager(old_obj).copy_fields(obj)


def get_translation_info(request):
    info = {'tg': request.get('persistent_tg'),
            'source_language': request.get('persistent_source_language')}
    if not info.get('tg') or not info.get('source_language'):
        raise AttributeError
    return info
