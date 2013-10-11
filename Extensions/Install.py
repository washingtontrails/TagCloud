from cStringIO import StringIO

from Products.Archetypes.Extensions.utils import install_subskin

from Products.TagCloud.config import *
from Products.TagCloud.Extensions.utils import *

def install(self):
    out = StringIO()

    install_subskin(self, out, GLOBALS)

    # Check that the tool has not been added using its id
    if not hasattr(self, TOOLNAME):
        addTool = self.manage_addProduct[PROJECTNAME].manage_addTool
        # Add the tool by its meta_type
        addTool('TagCloud Tool')

    # there doesn't seem to be a configlet yet.  Premature checkin, I guess.
    #removeConfiglet(self, out)
    #addConfiglet(self, out)

    addCacheManager(self, out)
    # this is a "classic" portlet.  we don't install them this way anymore
    #addPortlet(self, out)
    registerResources(self, out, 'portal_css', STYLESHEETS)
    registerResources(self, out, 'portal_javascripts', JAVASCRIPTS)

    print >> out, "Installation completed."
    return out.getvalue()


def uninstall(self):
    out = StringIO()

    #removeConfiglet(self, out)

    #removeCacheManager(self, out)
    #removePortlet(self, out)
    resetResources(self, out, 'portal_css', STYLESHEETS)
    resetResources(self, out, 'portal_javascripts', JAVASCRIPTS)

    print >> out, "TagCloud uninstalled."
    return out.getvalue()
