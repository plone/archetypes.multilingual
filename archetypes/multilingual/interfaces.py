# -*- coding: utf-8 -*-
from plone.app.multilingual.interfaces import ITranslatable
from zope.interface import Interface


class IArchetypesMultilingualInstalled(Interface):
    """ Marker interface """


class IArchetypesTranslatable(ITranslatable):
    """ translatable-marker for archetypes """
