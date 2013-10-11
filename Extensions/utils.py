from Products.CMFCore.utils import getToolByName
from Products.StandardCacheManagers import RAMCacheManager
from Products.TagCloud.config import *

import os, string


def addPortlet(self, out):
    """ add portlet to right slots """
    
    utool = getToolByName(self, 'portal_url')
    portal = utool.getPortalObject()
    portlets = list(portal.getProperty('right_slots'))
    
    for portlet in PORTLETS:
        if portlet not in portlets:
            portlets.insert(0, portlet)
    
    portal._updateProperty('right_slots', portlets)
 
    print >> out, 'Cached portlet added.\n'

def removePortlet(self, out):
    """remove portlet from right slots"""
    
    utool = getToolByName(self, 'portal_url')
    portal = utool.getPortalObject()
    portlets = list(portal.getProperty('right_slots'))
    
    for portlet in PORTLETS:
        if portlet in portlets:
            portlets.remove(portlet)
    
    portal._updateProperty('right_slots', portlets)
    
    print >> out, 'Cached portlet removed.\n'

def addCacheManager(self, out):
    """adds and associates RAM Cache Manager to portlet"""

    utool = getToolByName(self, 'portal_url')
    portal = utool.getPortalObject()

    meta_type = RAMCacheManager.RAMCacheManager.meta_type
    if CACHE_MANAGER not in portal.objectIds(meta_type):
        RAMCacheManager.manage_addRAMCacheManager(portal, CACHE_MANAGER)

    self[CACHE_MANAGER].manage_editProps(CACHE_MANAGER, CACHE_MANAGER_SETTINGS)

    print >> out, 'Cache Manager created.\n'

def removeCacheManager(self, out):
    """removes RAM Cache Manager"""
    if getattr(self, CACHE_MANAGER, None) is not None:
        self.manage_delObjects([CACHE_MANAGER])

        print >> out, 'Cache Manager deleted.\n'

def registerResources(self, out, toolname, resources):
    tool = getToolByName(self, toolname)
    existing = tool.getResourceIds()
    cook = False
    for resource in resources:
        if not resource['id'] in existing:
            # register additional resource in the specified registry
            if toolname == "portal_css":
                tool.registerStylesheet(**resource)
            if toolname == "portal_javascripts":
                tool.registerScript(**resource)
            print >> out, "Added %s to %s." % (resource['id'], tool)
        else:
            # or update existing ones
            parameters = tool.getResource(resource['id'])._data
            for key in [k for k in resource.keys() if k != 'id']:
                originalkey = 'original_'+key
                original = parameters.get(originalkey)
                if original:
                    original['products'] += 1
                else:
                    # keep original value for further reversion
                    parameters[originalkey] = { 'value': parameters[key],
                                                'products': 1 }
                parameters[key] = resource[key]
                print >> out, "Updated %s in %s." % (resource['id'], tool)
                cook = True
    if cook:
        tool.cookResources()
    print >> out, "Successfuly Installed/Updated resources in %s." % tool

def resetResources(self, out, tool, resources):
    # Revert resource customizations (only if this skin is the last DIY based
    # one to be uninstalled).
    tool = getToolByName(self, tool)
    for resource in [tool.getResource(r['id']) for r in resources]:
        parameters = resource._data
        for key in parameters.keys():
            originalkey = 'original_'+key
            original = parameters.get(originalkey)
            if original:
                if isinstance(original, dict):
                    original['products'] -= 1
                    if original['products'] == 0:
                        parameters[key] = original['value']
                        del parameters[originalkey]
                        print >> out, "Reset %s for %s." % (key,
                                                           parameters['id'])
                    else:
                        print >> out, "Left %s for %s unmolested for other DIY based skins" % (key, parameters['id'])
                else:  # backward compatibility with version prior to 2.1.1
                    parameters[key] = parameters[originalkey]
                    del parameters[originalkey]
                    print >> out, "Reset %s for %s." % (key, parameters['id'])

def addConfiglet(self, out):
    # add the configlets to the portal control panel
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in CONFIGLETS:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

def removeConfiglet(self, out):
    # remove the configlets from the portal control panel
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in CONFIGLETS:
            configTool.unregisterConfiglet(conf['id'])
            out.write('Removed configlet %s\n' % conf['id'])

__all__ = (
    "addPortlet",
    "removePortlet",
    "addCacheManager",
    "removeCacheManager",
    "registerResources",
    "resetResources",
    "addConfiglet",
    "removeConfiglet",
)
