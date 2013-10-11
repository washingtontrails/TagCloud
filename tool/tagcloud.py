# This Python file uses the following encoding: utf-8

__author__ = 'Héctor Velarde <hvelarde@jornada.com.mx>'
__docformat__ = 'restructuredtext'
__copyright__ = 'Copyright (C) 2006-2007  DEMOS, Desarrollo de Medios, S.A. de C.V.'
__license__  = 'The GNU General Public License version 2 or later'

from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from math import pow
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName, UniqueObject
from Products.TagCloud.config import LEVELS
from Products.TagCloud.interfaces import ITagCloudTool

class TagCloudTool(UniqueObject, SimpleItem):
    """ provides utility methods for Tag Cloud creation """
    implements(ITagCloudTool)

    id = 'tagcloud_tool'
    meta_type = title = 'TagCloud Tool'
    plone_tool = 1
    security = ClassSecurityInfo()

    def __init__(self):
        self.levels = LEVELS

    def _getCloudedTypes(self):
        """Return the list of content types that we care about for our our Tag Cloud"""
        return ["Blog Entry",]

    def _getTagsSorted(self):
        """ returns tags in alphabetical order; tags are subjects """

        catalog = getToolByName(self, 'portal_catalog')
        tags = list(catalog.uniqueValuesFor('Subject'))
        if tags:
            tags.sort(lambda x, y: cmp(x.lower(), y.lower()))
        return tuple(tags)

    def _getTagSize(self, tag, minWeight, maxWeight):
        """ returns normalized size for a given tag """

        #this algorithm was taken from Anders Pearson's blog: http://thraxil.com/users/anders/posts/2005/12/13/scaling-tag-clouds/
        thresholds = [pow(maxWeight - minWeight + 1, float(i) / float(self.levels)) for i in range(0, self.levels)]

        catalog = getToolByName(self, 'portal_catalog')
        #utils = getToolByName(self, 'plone_utils')
        #friendly_types = utils.getUserFriendlyTypes()
        friendly_types = self._getCloudedTypes()
        tagWeight = len(catalog.searchResults(Subject=tag, portal_type=friendly_types, review_state='published'))
        
        if tagWeight:
            size = 0
            for t in thresholds:
                size += 1
                if tagWeight <= t:
                    break
            return size
        return 0

    def _getMinWeight(self):
        """ returns number of times the least used tag was used """

        catalog = getToolByName(self, 'portal_catalog')
        # utils = getToolByName(self, 'plone_utils')
        # friendly_types = utils.getUserFriendlyTypes()
        friendly_types = self._getCloudedTypes()
        tags = catalog.uniqueValuesFor('Subject')
        if tags:
            weights = []
            for tag in tags:
                weight = len(catalog.searchResults(Subject=tag, portal_type=friendly_types, review_state='published'))
                if weight > 0:
                    weights.append(weight)
            if weights != []:
                return min(weights)
        return 0

    def _getMaxWeight(self):
        """ returns number of times the most used tag was used """

        catalog = getToolByName(self, 'portal_catalog')
        # utils = getToolByName(self, 'plone_utils')
        # friendly_types = utils.getUserFriendlyTypes()
        friendly_types = self._getCloudedTypes()
        tags = catalog.uniqueValuesFor('Subject')
        if tags:
            maxWeight = max([len(catalog.searchResults(Subject=tag, portal_type=friendly_types, review_state='published')) for tag in tags])
            return maxWeight
        return 0

    security.declarePublic('getCloud')
    def getCloud(self):
        """ returns a list of {tag, size} pairs in alphabetical order """

        cloud = []
        minWeight = self._getMinWeight();
        maxWeight = self._getMaxWeight();
        tags = self._getTagsSorted()
        for tag in tags:
            size = self._getTagSize(tag,minWeight,maxWeight)
            if size > 0:
                cloud.append({'tag': tag, 'size': size})
        return cloud

InitializeClass(TagCloudTool)
