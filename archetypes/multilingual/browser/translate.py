# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.app.multilingual import _
from plone.app.multilingual.browser.translate import google_translate
from plone.app.multilingual.interfaces import ILanguage
from plone.app.multilingual.interfaces import IMultiLanguageExtraOptionsSchema
from plone.app.multilingual.interfaces import ITranslationManager
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class gtranslation_service_at(BrowserView):

    def __call__(self):
        if (self.request.method != 'POST' and
            not ('field' in self.request.form.keys() and
                 'lang_source' in self.request.form.keys())):
            return _("Need a field")
        else:
            manager = ITranslationManager(self.context)
            registry = getUtility(IRegistry)
            settings = registry.forInterface(IMultiLanguageExtraOptionsSchema)
            lang_target = ILanguage(self.context).get_language()
            lang_source = self.request.form['lang_source']
            orig_object = manager.get_translation(lang_source)
            try:
                question = orig_object.getField(
                    self.request.form['field']).get(orig_object)
            except AttributeError:
                return _("Invalid field")
            return google_translate(
                question,
                settings.google_translation_key,
                lang_target, lang_source
            )
