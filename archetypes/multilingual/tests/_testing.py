# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
import doctest
from plone.app.testing import (
    PLONE_FIXTURE,
    PloneSandboxLayer,
    applyProfile,
    IntegrationTesting,
    FunctionalTesting,
)
from zope.configuration import xmlconfig


class ArchetypesMultilingualLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import archetypes.multilingual
        xmlconfig.file('configure.zcml', archetypes.multilingual,
                        context=configurationContext)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'archetypes.multilingual:default')

ARCHETYPESMULTILINGUAL_FIXTURE = ArchetypesMultilingualLayer()

ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING = IntegrationTesting(\
    bases=(ARCHETYPESMULTILINGUAL_FIXTURE,),\
    name="archetypes.multilingual:Integration")
ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING = FunctionalTesting(\
    bases=(ARCHETYPESMULTILINGUAL_FIXTURE,),\
    name="archetypes.multilingual:Functional")

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
