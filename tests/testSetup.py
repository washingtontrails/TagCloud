# This Python file uses the following encoding: utf-8

"""
this test suite was based on Martin Aspeli's 'borg' and David Convent's 'DIYPloneStyle' ones

tested on Zope 2.9.7 and Plone 2.5.3
"""

__author__ = 'Héctor Velarde <hvelarde@jornada.com.mx>'
__docformat__ = 'restructuredtext'
__copyright__ = 'Copyright (C) 2007  DEMOS, Desarrollo de Medios, S.A. de C.V.'
__license__  = 'The GNU General Public License version 2 or later'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Import the base test case classes
from base import TagCloudTestCase, PROJECTNAME

from Interface.Verify import verifyObject
from Products.TagCloud.config import *
from Products.TagCloud.interfaces import ITagCloudTool

class TestInstallation(TagCloudTestCase):
    """ ensure product is properly installed """

    def afterSetUp(self):
        self.tool       = self.portal.tagcloud_tool
        self.config     = self.portal.portal_controlpanel
        self.csstool    = self.portal.portal_css
        self.jstool     = self.portal.portal_javascripts
        self.kupu       = self.portal.kupu_library_tool
        self.skins      = self.portal.portal_skins
        self.types      = self.portal.portal_types
        self.factory    = self.portal.portal_factory
        self.workflow   = self.portal.portal_workflow
        self.properties = self.portal.portal_properties

    def testSkinLayersInstalled(self):
        """ test if skin layers are installed """
        self.failUnless('tagcloud_images' in self.skins.objectIds())
        self.failUnless('tagcloud_styles' in self.skins.objectIds())
        self.failUnless('tagcloud_templates' in self.skins.objectIds())

    def testCssInstalled(self):
        """ test if CSS are installed """
        stylesheetids = self.csstool.getResourceIds()
        for css in STYLESHEETS:
            self.failUnless(css['id'] in stylesheetids)

    def testJavascriptsInstalled(self):
        """ test if new javascripts were added to portal_javascripts """
        javascriptids = self.jstool.getResourceIds()
        for js in JAVASCRIPTS:
            self.failUnless(js['id'] in javascriptids)

    def testPortletInstalled(self):
        """ test if Cache Manager is installed """
        # portlets = list(self.portal.getProperty('right_slots'))
        # for portlet in PORTLETS:
        #     self.failUnless(portlet in portlets)
        pass

    def testCacheManagerInstalled(self):
        """ test if Cache Manager is installed """
        cache = getattr(self.portal, CACHE_MANAGER, None)
        self.failUnless(cache is not None)

    def testToolInstalled(self):
        self.failUnless(getattr(self.portal, 'tagcloud_tool', None) is not None)

    def _testConfiglet(self):
        """ test if Configlet is installed """
        configlets = list(self.config.listActions())
        for configlet in CONFIGLETS:
            self.failIf(configlet['id'] not in configlets)

class TestUninstall(TagCloudTestCase):

    def afterSetUp(self):
        """ uninstall requieres 'Manager' role """
        self.setRoles(['Manager', 'Member'])
        self.qitool = self.portal.portal_quickinstaller
        self.qitool.uninstallProducts(products=[PROJECTNAME])
        self.config = self.portal.portal_controlpanel

    def testProductUninstalled(self):
        """ test if the product was removed """
        self.failIf(self.qitool.isProductInstalled(PROJECTNAME))

    def testPortletUninstalled(self):
        """ test if Cache Manager was removed """
        # portlets = list(self.portal.getProperty('right_slots'))
        # for portlet in PORTLETS:
        #     self.failIf(portlet in portlets)
        pass

    def testCacheManagerUninstalled(self):
        """ test if Cache Manager was removed """
        cache = getattr(self.portal, CACHE_MANAGER, None)
        self.failUnless(cache is None)

    def testToolUninstalled(self):
        self.failIf(getattr(self.portal, 'tagcloud_tool', None) is not None)

    def testConfigletUninstalled(self):
        """ test if Configlet was removed """
        configlets = list(self.config.listActions())
        for configlet in CONFIGLETS:
            self.failIf(configlet['id'] in configlets)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    suite.addTest(makeSuite(TestUninstall))
    return suite

if __name__ == '__main__':
    framework()
