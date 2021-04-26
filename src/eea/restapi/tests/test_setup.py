# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest
from eea.restapi.testing import EEA_RESTAPI_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that eea.restapi is properly installed."""

    layer = EEA_RESTAPI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if eea.restapi is installed."""
        self.assertTrue(self.installer.isProductInstalled('eea.restapi'))

    def test_browserlayer(self):
        """Test that IEEARestapiLayer is registered."""
        from eea.restapi.interfaces import IEEARestapiLayer
        from plone.browserlayer import utils

        self.assertIn(IEEARestapiLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    ''' test uninstall '''

    layer = EEA_RESTAPI_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['eea.restapi'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if eea.restapi is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('eea.restapi'))

    def test_browserlayer_removed(self):
        """Test that IEEARestapiLayer is removed."""
        from eea.restapi.interfaces import IEEARestapiLayer
        from plone.browserlayer import utils

        self.assertNotIn(IEEARestapiLayer, utils.registered_layers())
