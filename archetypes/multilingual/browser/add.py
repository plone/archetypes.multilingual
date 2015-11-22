# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone import api


class MultilingualATAddForm(BrowserView):

    def __call__(self):
        """ Copy from createObject.cpy
        """
        response = self.request.response
        response.setHeader('Expires', 'Sat, 01 Jan 2000 00:00:00 GMT')
        response.setHeader('Cache-Control', 'no-cache')

        original_object = self._get_original_object()
        type_name = original_object.portal_type

        self.tg = original_object.TranslationGroup
        self.source_language = original_object.Language
        self._redirect(type_name)

    def _set_translation_info(self):
        self.request.translation_info

    def _get_original_object(self):
        uid = self.request.get('type', None)

        if uid is None:
            raise Exception('Original object not specified')

        catalog = api.portal.get_tool(name='portal_catalog')
        return catalog(UID=uid)[0]

    def _redirect(self, type_name):
        id = self.context.generateUniqueId(type_name)
        types_tool = getToolByName(self.context, 'portal_types')

        fti = types_tool.getTypeInfo(type_name)
        if fti is None:
            raise KeyError("Type name not found: %s." % type_name)
            # state.setStatus('success_no_edit')

        if type_name in self.context.portal_factory.getFactoryTypes():
            new_url = 'portal_factory/' + type_name + '/' + id + '/at_babel_edit'
            new_url = '%s?tg=%s&source_language=%s' % (new_url,
                                                       self.tg,
                                                       self.source_language)
            return self.request.response.redirect(new_url)
            # state.set(status='factory',
            #           next_action='redirect_to:string:%s' % new_url)
            # If there's an issue with object creation, let the factory
            # handle it
            # return state
        else:
            new_id = self.context.invokeFactory(id=id, type_name=type_name)
            if new_id is None or new_id == '':
                new_id = id
            o = getattr(self.context, new_id, None)

        if o is None:
            raise Exception

        return self.request.response.redirect(o.absolute_url())
