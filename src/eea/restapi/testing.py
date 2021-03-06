# -*- coding: utf-8 -*-
''' testing module - define layers '''
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import eea.restapi


class EEARestapiLayer(PloneSandboxLayer):
    ''' EEA Restapi Layer '''

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        ''' Load any other ZCML that is required for your tests.
        The z3c.autoinclude feature is disabled in the Plone fixture base
        layer. '''
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=eea.restapi)

    def setUpPloneSite(self, portal):
        ''' setUp Plone Site '''
        applyProfile(portal, 'eea.restapi:default')


EEA_RESTAPI_FIXTURE = EEARestapiLayer()


EEA_RESTAPI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_RESTAPI_FIXTURE,),
    name='EEARestapiLayer:IntegrationTesting',
)


EEA_RESTAPI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEA_RESTAPI_FIXTURE,),
    name='EEARestapiLayer:FunctionalTesting',
)


EEA_RESTAPI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EEA_RESTAPI_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EEARestapiLayer:AcceptanceTesting',
)
