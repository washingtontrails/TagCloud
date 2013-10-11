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

from Products.CMFCore.utils import UniqueObject
from Interface.Verify import verifyObject
from OFS.interfaces import ISimpleItem
from Products.Archetypes.interfaces import IBaseFolder

from Products.TagCloud.config import *
from Products.TagCloud.interfaces import ITagCloudTool

class TestCloudCreation(TagCloudTestCase):
    """ ensure tag cloud is generated """

    def _publish(self):
        self.setRoles(['Manager', 'Member'])
        self.workflow.doActionFor(self.o1, 'publish')
        # images don't have WF
        # self.workflow.doActionFor(self.o2, 'publish')
        # self.workflow.doActionFor(self.o3, 'publish')
        self.workflow.doActionFor(self.o4, 'publish')
        self.workflow.doActionFor(self.o5, 'publish')
        self.workflow.doActionFor(self.o6, 'publish')
        self.workflow.doActionFor(self.o7, 'publish')
        self.workflow.doActionFor(self.o8, 'publish')

    def _setFriendlyTypes(self, friendly_types):
        allTypes = self.portal.getPortalTypes()
        blacklistedTypes = [t for t in allTypes if t not in friendly_types]
        self.properties.site_properties.manage_changeProperties(types_not_searched=blacklistedTypes)

    def afterSetUp(self):
        self.tool       = self.portal.tagcloud_tool
        self.properties = self.portal.portal_properties
        self.utils      = self.portal.plone_utils
        self.workflow   = self.portal.portal_workflow

        friendly_types = ['Document','Image','News Item']
        self._setFriendlyTypes(friendly_types)

        self.folder.invokeFactory('Document', 'o1')
        self.folder.invokeFactory('Image', 'o2')
        self.folder.invokeFactory('Image', 'o3')
        self.folder.invokeFactory('News Item', 'o4')
        self.folder.invokeFactory('News Item', 'o5')
        self.folder.invokeFactory('News Item', 'o6')
        self.folder.invokeFactory('Event', 'o7')
        self.folder.invokeFactory('Folder', 'o8')
        self.o1 = getattr(self.folder, 'o1')
        self.o2 = getattr(self.folder, 'o2')
        self.o3 = getattr(self.folder, 'o3')
        self.o4 = getattr(self.folder, 'o4')
        self.o5 = getattr(self.folder, 'o5')
        self.o6 = getattr(self.folder, 'o6')
        self.o7 = getattr(self.folder, 'o7')
        self.o8 = getattr(self.folder, 'o8')
        self.o1.update(subject='one')
        self.o2.update(subject='two')
        self.o3.update(subject='two')
        self.o4.update(subject='three')
        self.o5.update(subject='three')
        self.o6.update(subject='three')
        self.o7.update(subject='four')
        self.o8.update(subject='four')

    def testGetTagsSorted(self):
        """ test if unique tags are returned in alphabetical order """
        TAGS = ('four','one','three','two')
        tags = self.tool._getTagsSorted()
        self.assertEqual(len(tags), 4)
        for tag, TAG in zip(tags, TAGS):
            self.assertEqual(tag, TAG)

        # publishing items doesn't affect tags, neither order
        self._publish()
        tags = self.tool._getTagsSorted()
        self.assertEqual(len(tags), 4)
        for tag, TAG in zip(tags, TAGS):
            self.assertEqual(tag, TAG)

    def testGetMinWeight(self):
        """ test if items are counted """
        self.assertEqual(self.tool._getMinWeight(), 0)

        self._publish()
        min = self.tool._getMinWeight()
        self.assertEqual(min, 1)

    def testGetMaxWeight(self):
        """ test if items are counted """
        self.assertEqual(self.tool._getMaxWeight(), 0)

        self._publish()
        max = self.tool._getMaxWeight()
        self.assertEqual(max, 3)

    def testGetTagSize(self):
        """ test if tag size is calculated """
        minWeight = self.tool._getMinWeight()
        maxWeight = self.tool._getMaxWeight()
        self.assertEqual(self.tool._getTagSize('one', minWeight, maxWeight), 0)
        self.assertEqual(self.tool._getTagSize('two', minWeight, maxWeight), 0)
        self.assertEqual(self.tool._getTagSize('three', minWeight, maxWeight), 0)

        self._publish()
        minWeight = self.tool._getMinWeight()
        maxWeight = self.tool._getMaxWeight()
        self.assertEqual(self.tool._getTagSize('one', minWeight, maxWeight), 1)
        # images are tagged as "two"
        #self.assertEqual(self.tool._getTagSize('two', minWeight, maxWeight), 5)
        self.assertEqual(self.tool._getTagSize('three', minWeight, maxWeight), 5)

    def testCloud(self):
        """ test tag cloud list """
        CLOUD = []
        cloud = self.tool.getCloud()
        self.assertEqual(cloud, CLOUD)

        self._publish()
        CLOUD = [{'tag': 'one', 'size': 1},
                 {'tag': 'three', 'size': 5},
                 #{'tag': 'two', 'size': 5},
                 ]
        cloud = self.tool.getCloud()
        self.assertEqual(cloud, CLOUD)

class TestToolClass(TagCloudTestCase):
    """ ensure tool implementation """

    def afterSetUp(self):
        self.tool = self.portal.tagcloud_tool

    def testIsUniqueObject(self):
        self.failUnless(isinstance(self.tool, UniqueObject))

    def testImplementsSimpleItem(self):
        iface = ISimpleItem
        self.failUnless(iface.isImplementedBy(self.tool))
        self.failUnless(verifyObject(iface, self.tool))

    def testImplementsTagCloudTool(self):
        iface = ITagCloudTool
        self.failUnless(iface.isImplementedBy(self.tool))
        self.failUnless(verifyObject(iface, self.tool))

    def testToolNames(self):
        """ test if tool names are correct """
        t = self.tool
        self.failUnlessEqual(t.meta_type, 'TagCloud Tool')
        self.failUnlessEqual(t.getId(), TOOLNAME)
        self.failUnlessEqual(t.title, 'TagCloud Tool')
        self.failUnlessEqual(t.plone_tool, True)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCloudCreation))
    suite.addTest(makeSuite(TestToolClass))
    return suite

if __name__ == '__main__':
    framework()
