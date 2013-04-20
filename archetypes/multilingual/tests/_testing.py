# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
import doctest
import transaction
from OFS.Folder import Folder
from Testing import ZopeTestCase as ztc

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

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import archetypes.multilingual
        import archetypes.testcase

        xmlconfig.file('testing.zcml', archetypes.multilingual,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', archetypes.testcase,
                       context=configurationContext)

        z2.installProduct(app, 'archetypes.testcase')

        # Support sessionstorage in tests
        app.REQUEST['SESSION'] = self.Session()
        if not hasattr(app, 'temp_folder'):
            tf = Folder('temp_folder')
            app._setObject('temp_folder', tf)
            transaction.commit()

        ztc.utils.setupCoreSessions(app)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'archetypes.multilingual:testing')
        applyProfile(portal, 'archetypes.testcase:default')

ARCHETYPESMULTILINGUAL_FIXTURE = ArchetypesMultilingualLayer()

ARCHETYPESMULTILINGUAL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ARCHETYPESMULTILINGUAL_FIXTURE,),
    name="archetypes.multilingual:Integration")
ARCHETYPESMULTILINGUAL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ARCHETYPESMULTILINGUAL_FIXTURE,),
    name="archetypes.multilingual:Functional")

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
