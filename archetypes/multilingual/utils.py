# -*- coding: utf-8 -*-
from plone.app.multilingual.interfaces import ILanguageIndependentFieldsManager
from zope import interface


class LanguageIndependentFieldsManager(object):
    interface.implements(ILanguageIndependentFieldsManager)

    def __init__(self, context):
        self.context = context

    def _copy_field(self, field, translation):
        accessor = field.getEditAccessor(self.context)
        if not accessor:
            accessor = field.getAccessor(self.context)
        if accessor:
            data = accessor()
        else:
            data = field.get(self.context)
        mutator = field.getMutator(translation)
        if mutator is not None:
            # Protect against weird fields, like computed fields
            mutator(data)
        else:
            field.set(translation, data)

    def copy_fields(self, translation):
        dest_schema = translation.Schema()
        schema = self.context.Schema()
        fields = schema.filterFields(languageIndependent=True)
        fields_to_copy = [x for x in fields if x.getName() in dest_schema]
        for field in fields_to_copy:
            self._copy_field(field, translation)
