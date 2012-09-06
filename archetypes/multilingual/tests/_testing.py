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
from plone.testing import z2


class ArchetypesMultilingualLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import archetypes.multilingual
        import archetypes.testcase

        xmlconfig.file('configure.zcml', archetypes.multilingual,
                        context=configurationContext)
        xmlconfig.file('configure.zcml', archetypes.testcase,
                        context=configurationContext)

        z2.installProduct(app, 'archetypes.testcase')

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'archetypes.multilingual:default')
        applyProfile(portal, 'archetypes.testcase:default')

ARCHETYPESMULTILINGUAL_FIXTURE = ArchetypesMultilingualLayer()

ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING = IntegrationTesting(\
    bases=(ARCHETYPESMULTILINGUAL_FIXTURE,),\
    name="archetypes.multilingual:Integration")
ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING = FunctionalTesting(\
    bases=(ARCHETYPESMULTILINGUAL_FIXTURE,),\
    name="archetypes.multilingual:Functional")

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
